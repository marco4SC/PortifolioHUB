"""
Classe base para todos os agentes de IA.
"""
from dataclasses import dataclass, field
from typing import Any
import anthropic
from config import config

@dataclass
class AgentSignal:
    agent_name: str
    asset: str
    signal: str           # "BUY" | "SELL" | "HOLD" | "AVOID"
    confidence: float     # 0.0 a 1.0
    reasoning: str
    data_points: dict
    timestamp: str = field(default_factory=lambda: __import__('datetime').datetime.now().isoformat())

class BaseAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)

    def _call_llm(self, user_message: str, max_tokens: int = 1000) -> str:
        response = self.client.messages.create(
            model=config.llm_model,
            max_tokens=max_tokens,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def analyze(self, asset: str, data: dict) -> AgentSignal:
        raise NotImplementedError