import pytest

from core.llm.ollama.client import OllamaClient
from core.llm.ollama.provider import OllamaProvider

from core.llm.config import LLMConfig
from core.llm.models import LLMRequest


@pytest.mark.asyncio
async def test_real_ollama_provider():

    provider = OllamaProvider(
        OllamaClient(),
        LLMConfig(
            model="llama3.2:3b"
        )
    )

    result = await provider.complete(
        LLMRequest(
            prompt="Say hello to Purrfect"
        )
    )

    assert result.content
    assert result.model == "llama3.2:3b"