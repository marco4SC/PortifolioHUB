"""
Fonte de dados de mercado — preços, OHLC, volume.
Usa brapi.dev para ações BR e CoinGecko para cripto (ambas gratuitas).
"""
import requests
import pandas as pd
from datetime import datetime
from typing import Optional
import time

BRAPI_BASE = "https://brapi.dev/api"
COINGECKO_BASE = "https://api.coingecko.com/api/v3"

class MarketDataSource:
    def __init__(self, brapi_token: str = ""):
        self.brapi_token = brapi_token
        self._cache: dict = {}
        self._cache_ttl = 60

    def _cached(self, key: str, fetch_fn, ttl: int = 60):
        now = time.time()
        if key in self._cache:
            data, ts = self._cache[key]
            if now - ts < ttl:
                return data
        data = fetch_fn()
        self._cache[key] = (data, now)
        return data

    def get_stock_quote(self, ticker: str) -> dict:
        def fetch():
            url = f"{BRAPI_BASE}/quote/{ticker}"
            params = {"token": self.brapi_token} if self.brapi_token else {}
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            result = data["results"][0]
            return {
                "ticker": ticker,
                "price": result["regularMarketPrice"],
                "change_pct": result["regularMarketChangePercent"],
                "volume": result["regularMarketVolume"],
                "market_cap": result.get("marketCap"),
                "pe_ratio": result.get("priceEarningsRatio"),
                "timestamp": datetime.now().isoformat(),
            }
        return self._cached(f"stock_{ticker}", fetch, ttl=60)

    def get_stock_history(self, ticker: str, period: str = "3mo", interval: str = "1d") -> pd.DataFrame:
        url = f"{BRAPI_BASE}/quote/{ticker}"
        params = {
            "range": period,
            "interval": interval,
            "token": self.brapi_token,
        }
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        hist = data["results"][0].get("historicalDataPrice", [])
        if not hist:
            return pd.DataFrame()
        df = pd.DataFrame(hist)
        df["date"] = pd.to_datetime(df["date"], unit="s")
        df = df.set_index("date").sort_index()
        df.columns = [c.lower() for c in df.columns]
        return df[["open", "high", "low", "close", "volume"]]

    def get_crypto_price(self, symbol: str) -> dict:
        id_map = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana"}
        coin_id = id_map.get(symbol.upper(), symbol.lower())

        def fetch():
            url = f"{COINGECKO_BASE}/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd,brl",
                "include_24hr_change": "true",
                "include_market_cap": "true",
            }
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()[coin_id]
            return {
                "symbol": symbol,
                "price_usd": data["usd"],
                "price_brl": data["brl"],
                "change_24h": data.get("usd_24h_change", 0),
                "market_cap_usd": data.get("usd_market_cap"),
                "timestamp": datetime.now().isoformat(),
            }
        return self._cached(f"crypto_{symbol}", fetch, ttl=120)

    def get_multiple_quotes(self, tickers: list) -> list:
        url = f"{BRAPI_BASE}/quote/{','.join(tickers)}"
        params = {"token": self.brapi_token} if self.brapi_token else {}
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        results = r.json()["results"]
        return [
            {
                "ticker": item["symbol"],
                "price": item["regularMarketPrice"],
                "change_pct": item["regularMarketChangePercent"],
                "volume": item["regularMarketVolume"],
            }
            for item in results
        ]