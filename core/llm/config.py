from dataclasses import dataclass


@dataclass
class LLMConfig:

    model: str

    temperature: float = 0.7

    timeout: int = 30