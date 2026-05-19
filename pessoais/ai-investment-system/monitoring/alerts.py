"""
Sistema de alertas via Telegram.
"""
import requests
from datetime import datetime
from config import config

TELEGRAM_API = f"https://api.telegram.org/bot{config.telegram_token}"

def send_telegram(message: str, parse_mode: str = "Markdown") -> bool:
    if not config.telegram_token or not config.telegram_chat_id:
        print(f"[ALERT]\n{message}")
        return False
    try:
        r = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": config.telegram_chat_id,
                "text": message,
                "parse_mode": parse_mode,
            },
            timeout=10,
        )
        return r.status_code == 200
    except Exception as e:
        print(f"Erro no Telegram: {e}")
        return False

def alert_decision(decision) -> None:
    signal_emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡", "AVOID": "⚫"}.get(decision.final_signal, "⚪")
    msg = f"""
{signal_emoji} *DECISÃO: {decision.final_signal} — {decision.asset}*

📊 Confiança: `{decision.consolidated_confidence:.0%}`
💼 Posição sugerida: `{decision.position_size_pct:.0%}` do portfólio
🎯 Preço-alvo: `R$ {decision.price_target:.2f}`
🛑 Stop-loss: `R$ {decision.stop_loss:.2f}`
⏳ Horizonte: `{decision.time_horizon}`

📝 *Tese:*
{decision.investment_thesis[:400]}

⚠️ *Riscos:*
{chr(10).join(f'• {r}' for r in decision.key_risks[:3])}

🚀 *Catalisadores:*
{chr(10).join(f'• {c}' for c in decision.catalysts[:2])}

_AI Investment System · {datetime.now().strftime("%d/%m/%Y %H:%M")}_
"""
    send_telegram(msg)

def alert_stop_triggered(asset: str, current_price: float, stop_price: float) -> None:
    msg = f"""
🔴 *STOP-LOSS ATIVADO: {asset}*

Preço atual: `R$ {current_price:.2f}`
Stop definido: `R$ {stop_price:.2f}`
Perda: `{(current_price/stop_price - 1)*100:.1f}%`

Ação: *VENDA IMEDIATA*
_{datetime.now().strftime("%d/%m/%Y %H:%M")}_
"""
    send_telegram(msg)

def alert_drawdown_breach(current_value: float, peak_value: float, drawdown_pct: float) -> None:
    msg = f"""
🚨 *ALERTA DE DRAWDOWN MÁXIMO*

Portfólio em `{drawdown_pct:.1f}%` abaixo do pico
Valor atual: `R$ {current_value:,.2f}`
Pico: `R$ {peak_value:,.2f}`

Ação: Revisar todas as posições.
_{datetime.now().strftime("%d/%m/%Y %H:%M")}_
"""
    send_telegram(msg)