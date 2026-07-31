from dataclasses import dataclass


@dataclass
class LLMRequest:

    prompt: str

    system_prompt: str | None = None

    metadata: dict | None = None



@dataclass
class LLMResponse:

    content: str

    model: str | None = None

    metadata: dict | None = None