import pytest

from core.llm.ollama import OllamaProvider
from core.llm.models import LLMRequest
from core.llm.config import LLMConfig


class FakeOllamaClient:

    async def chat(
        self,
        model,
        messages
    ):
        return {
            "message": {
                "content": "ollama response"
            }
        }


@pytest.mark.asyncio
async def test_ollama_provider_returns_response():

    provider = OllamaProvider(
        FakeOllamaClient(),
        LLMConfig(
            model="llama3"
        )
    )


    result = await provider.complete(
        LLMRequest(
            prompt="hello"
        )
    )


    assert result.content == "ollama response"
    assert result.model == "llama3"