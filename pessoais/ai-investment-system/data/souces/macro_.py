"""
Dados macroeconômicos do Banco Central do Brasil (SGS).
Gratuito, sem autenticação.
"""
import requests
import pandas as pd
from datetime import datetime, timedelta

BCB_SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados"

SERIES = {
    "selic_meta": 432,
    "selic_diaria": 11,
    "ipca_mensal": 433,
    "cambio_usd_brl": 1,
    "igpm_mensal": 189,
    "pib_crescimento": 4380,
    "inadimplencia": 21082,
}

def get_bcb_series(series_name: str, days: int = 365) -> pd.Series:
    serie_id = SERIES[series_name]
    end = datetime.now()
    start = end - timedelta(days=days)
    url = BCB_SGS.format(serie_id)
    params = {
        "formato": "json",
        "dataInicial": start.strftime("%d/%m/%Y"),
        "dataFinal": end.strftime("%d/%m/%Y"),
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    s = pd.Series(
        {
            datetime.strptime(d["data"], "%d/%m/%Y"): float(d["valor"].replace(",", "."))
            for d in data
        }
    )
    s.name = series_name
    return s.sort_index()

def get_macro_snapshot() -> dict:
    snapshot = {}
    for name in ["selic_meta", "ipca_mensal", "cambio_usd_brl"]:
        try:
            s = get_bcb_series(name, days=60)
            snapshot[name] = {
                "latest": float(s.iloc[-1]),
                "prev": float(s.iloc[-2]) if len(s) > 1 else None,
                "date": s.index[-1].strftime("%Y-%m-%d"),
            }
        except Exception as e:
            snapshot[name] = {"error": str(e)}
    return snapshot