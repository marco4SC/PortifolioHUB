"""
Agente de Sentimento.
Analisa notícias via RSS e classifica sentimento com LLM.
"""
import json
import feedparser
from agents.base import BaseAgent, AgentSignal

SYSTEM_PROMPT = """Você é um analista de sentimento especializado em mercados financeiros brasileiros.
Receberá títulos e trechos de notícias recentes sobre um ativo e deve:

1. Classificar o sentimento de cada notícia (positivo/negativo/neutro)
2. Pesar pela relevância e recência
3. Identificar eventos de alta relevância
4. Avaliar se o sentimento é temporário ou estrutural

Retorne APENAS JSON:
{
  "signal": "BUY|SELL|HOLD|AVOID",
  "confidence": 0.0,
  "overall_sentiment": "positive|negative|neutral",
  "sentiment_score": 0.0,
  "reasoning": "análise detalhada",
  "key_events": ["evento1", "evento2"]
}"""

RSS_FEEDS = [
    "https://www.infomoney.com.br/feed/",
    "https://br.investing.com/rss/news.rss",
]

COMPANY_MAP = {
    "PETR4": "Petrobras", "VALE3": "Vale", "ITUB4": "Itaú",
    "BBDC4": "Bradesco", "WEGE3": "WEG", "ABEV3": "Ambev",
    "RENT3": "Localiza", "B3SA3": "B3",
}

def fetch_news(query: str, max_items: int = 15) -> list:
    news = []
    query_lower = query.lower()
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:30]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                if query_lower in title.lower() or query_lower in summary.lower():
                    news.append({
                        "title": title,
                        "summary": summary[:300],
                        "published": entry.get("published", ""),
                    })
                    if len(news) >= max_items:
                        break
        except Exception:
            continue
    return news

class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__("SentimentAgent", SYSTEM_PROMPT)

    def analyze(self, asset: str, data: dict = None) -> AgentSignal:
        if data and "news" in data:
            news = data["news"]
        else:
            search_term = COMPANY_MAP.get(asset, asset)
            news = fetch_news(search_term)

        if not news:
            return AgentSignal(self.name, asset, "HOLD", 0.3,
                             "Sem notícias recentes", {"news_count": 0})

        news_text = "\n".join([
            f"- {n['title']} ({n['published']}): {n['summary']}"
            for n in news
        ])

        prompt = f"Analise o sentimento das notícias recentes sobre {asset}:\n\n{news_text}\n\nRetorne o JSON."

        try:
            response = self._call_llm(prompt, max_tokens=800)
            clean = response.strip().strip("```json").strip("```").strip()
            result = json.loads(clean)
            return AgentSignal(
                agent_name=self.name,
                asset=asset,
                signal=result["signal"],
                confidence=float(result["confidence"]),
                reasoning=result["reasoning"],
                data_points={
                    "news_count": len(news),
                    "overall_sentiment": result.get("overall_sentiment"),
                    "sentiment_score": result.get("sentiment_score"),
                    "key_events": result.get("key_events", []),
                },
            )
        except Exception as e:
            return AgentSignal(self.name, asset, "HOLD", 0.0, f"Erro: {e}", {})