import pytest

from core.llm.service import LLMService
from core.llm.provider import LLMProvider
from core.llm.models import (
    LLMRequest,
    LLMResponse
)


class FakeLLMProvider:

    async def complete(
        self,
        request: LLMRequest
    ) -> LLMResponse:

        return LLMResponse(
            content="fake llm response",
            model="fake"
        )


@pytest.mark.asyncio
async def test_llm_service_calls_provider():

    provider = FakeLLMProvider()

    service = LLMService(
        provider
    )


    result = await service.complete(
        "hello"
    )


    assert result.content == "fake llm response"

    assert result.model == "fake"