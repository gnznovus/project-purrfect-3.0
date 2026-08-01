from ..models import (
    LLMRequest,
    LLMResponse
)

from ..provider import LLMProvider
from core.llm.config import LLMConfig
from core.config.llm import (
    OLLAMA_MODEL,
    LLM_TEMPERATURE,
    LLM_TIMEOUT
)

config = LLMConfig(
    model=OLLAMA_MODEL,
    temperature=LLM_TEMPERATURE,
    timeout=LLM_TIMEOUT
)

class OllamaProvider(LLMProvider):

    def __init__(
        self,
        client,
        config: LLMConfig,
    ):
        self.client = client
        self.config = config


    async def complete(
        self,
        request: LLMRequest
    ) -> LLMResponse:

        response = await self.client.chat(
            model=self.config.model,
            messages=[
                {
                    "role": "user",
                    "content": request.prompt
                }
            ]
        )


        return LLMResponse(
            content=response["message"]["content"],
            model=self.config.model
        )