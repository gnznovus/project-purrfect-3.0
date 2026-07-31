from .models import (
    LLMRequest,
    LLMResponse
)

from .provider import LLMProvider


class LLMService:

    def __init__(
        self,
        provider: LLMProvider
    ):
        self.provider = provider


    async def complete(
        self,
        prompt: str
    ) -> LLMResponse:

        return await self.provider.complete(
            LLMRequest(
                prompt=prompt
            )
        )