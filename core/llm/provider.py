from abc import ABC, abstractmethod

from .models import (
    LLMRequest,
    LLMResponse
)


class LLMProvider(ABC):

    @abstractmethod
    async def complete(
        self,
        request: LLMRequest
    ) -> LLMResponse:
        pass