# 🤖 AI Investment System

> Sistema multiagente de inteligência artificial para análise e suporte a decisões de investimento em múltiplos ativos (ações BR, criptomoedas e renda fixa).

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Claude API](https://img.shields.io/badge/Claude%20API-Sonnet%204-CC785C?style=flat)](https://anthropic.com)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=flat)](https://github.com/marco4SC/PortfolioHUB)

---

## 📐 Arquitetura

```
Fontes de dados (B3, BCB, CoinGecko, RSS)
        ↓
  Data Pipeline (ETL, cache Redis, TimescaleDB)
        ↓
┌─────────────────────────────────────────┐
│         Agentes Especializados (LLM)    │
│  📈 Técnico  │  📊 Fundamentalista      │
│  📰 Sentimento │  🌍 Macro & Risco      │
└─────────────────────────────────────────┘
        ↓
  Orquestrador — "Chief Investment Officer IA"
  (agrega sinais, gera tese de investimento)
        ↓
  Gestão de Portfólio (Markowitz, Risk Parity)
        ↓
  Monitoramento + Alertas Telegram
```

---

## 🧠 Agentes de IA

| Agente | Responsabilidade | Indicadores |
|---|---|---|
| **Técnico** | Análise de preço e padrões | RSI, MACD, Bollinger Bands, Médias móveis, Volume |
| **Fundamentalista** | Valuation e qualidade do negócio | P/L, P/VPA, ROE, ROIC, Dívida/EBITDA, DY |
| **Sentimento** | NLP em notícias e redes sociais | Score de sentimento, eventos-chave, intensidade |
| **Macro & Risco** | Ambiente macroeconômico | Selic, IPCA, câmbio, taxa real, correlações |
| **Orquestrador** | Decisão final com tese auditável | Sinal consolidado, stop-loss, preço-alvo, sizing |

---

## 🗂️ Estrutura do projeto

```
ai-investment-system/
├── data/
│   └── sources/
│       ├── market.py        # Preços via brapi.dev e CoinGecko
│       ├── macro.py         # BCB/SGS: Selic, IPCA, câmbio
│       ├── news.py          # RSS financeiro
│       └── onchain.py       # Dados on-chain para cripto
├── agents/
│   ├── base.py              # Classe base + AgentSignal
│   ├── technical.py         # Análise técnica + cálculo de indicadores
│   ├── fundamental.py       # Valuation fundamentalista
│   ├── sentiment.py         # NLP em notícias
│   ├── macro.py             # Avaliação macroeconômica
│   └── orchestrator.py      # Orquestrador CIO
├── portfolio/
│   ├── optimizer.py         # Markowitz + Risk Parity (scipy)
│   ├── risk.py              # Stop-loss, VaR, drawdown, Kelly sizing
│   └── executor.py          # Execução e backtesting
├── monitoring/
│   └── alerts.py            # Alertas via Telegram Bot API
├── api/
│   └── main.py              # FastAPI REST API
├── config.py                # Configurações centralizadas
├── requirements.txt
└── .env.example
```

---

## 🚀 Como executar

```bash
# 1. Clone e entre na pasta
git clone https://github.com/marco4SC/PortfolioHUB.git
cd PortfolioHUB/projetos/ai-investment-system

# 2. Ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac | venv\Scripts\activate no Windows

# 3. Dependências
pip install -r requirements.txt

# 4. Configuração
cp .env.example .env
# Edite .env com sua ANTHROPIC_API_KEY

# 5. Iniciar a API
uvicorn api.main:app --reload --port 8000

# 6. Testar análise
curl -X POST http://localhost:8000/analyze/PETR4
```

---

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/health` | Status do sistema |
| `GET` | `/market/quotes?tickers=PETR4,VALE3` | Cotações em tempo real |
| `GET` | `/macro/snapshot` | Selic, IPCA, câmbio atuais |
| `POST` | `/analyze/{ticker}` | Análise completa com todos os agentes |
| `GET` | `/portfolio/summary` | Resumo do portfólio |

### Exemplo de resposta — `POST /analyze/VALE3`

```json
{
  "asset": "VALE3",
  "final_signal": "BUY",
  "consolidated_confidence": 0.74,
  "position_size_pct": 0.12,
  "price_target": 68.50,
  "stop_loss": 57.20,
  "time_horizon": "medium",
  "investment_thesis": "VALE3 apresenta valuaton atrativo (P/L 5.8x vs. histórico 7.2x) com suporte técnico em R$59...",
  "key_risks": ["Queda do minério de ferro", "Risco cambial BRL/USD", "Ambiente macro restritivo"],
  "catalysts": ["Resultado 2T25 acima do esperado", "Retomada chinesa"],
  "consensus_score": 0.81
}
```

---

## 🛠️ Stack tecnológico

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **IA/LLM**: Anthropic Claude (claude-sonnet-4)
- **Dados**: brapi.dev, CoinGecko API, BCB/SGS API, feedparser
- **Análise**: Pandas, NumPy, Scipy (otimização de portfólio)
- **Armazenamento**: SQLite (dev) → TimescaleDB (produção)
- **Cache**: Redis
- **Alertas**: Telegram Bot API
- **Deploy**: GitHub Pages (docs) + VPS (API)

---

## 🗺️ Roadmap

- [x] Data pipeline com APIs gratuitas (brapi, CoinGecko, BCB)
- [x] 4 agentes especializados com Claude API
- [x] Orquestrador com tese de investimento auditável
- [x] Gestão de risco (stop-loss, VaR, Kelly sizing)
- [x] Otimização de portfólio (Markowitz + Risk Parity)
- [x] API REST com FastAPI
- [x] Alertas via Telegram
- [ ] Dashboard React com Recharts
- [ ] Backtesting com dados históricos
- [ ] Scheduler para análises automáticas diárias
- [ ] Paper trading automatizado
- [ ] Integração com corretora (XP/Clear API)
- [ ] Deploy em VPS com CI/CD

---

## ⚠️ Aviso importante

Este sistema é uma **ferramenta de apoio à decisão**, não um consultor de investimentos registrado. Nenhum algoritmo garante retorno positivo. Sempre use gestão de risco, nunca invista mais do que pode perder, e comece com **paper trading** antes de usar capital real.

---

## 👨‍💻 Autor

**Marco Antonio de Souza Carvalho**  
Estudante de Engenharia da Computação — UniCEUB  
[LinkedIn](https://linkedin.com/in/marco-antonio-souza-carvalho-614bb3329) · [Portfólio](https://marco4sc.github.io/PortfolioHUB/)
