import pytest

from core.engine import CoreEngine
from core.router import Router

from core.context_builder import ContextBuilder

from core.conversation.mode import ConversationMode
from core.conversation.state import ConversationState

from core.handlers.chitchat import ChitchatHandler

from core.llm.service import LLMService
from core.llm.config import LLMConfig
from core.llm.ollama.client import OllamaClient
from core.llm.ollama.provider import OllamaProvider
from core.llm.models import LLMResponse

from ..utils.trace import write_trace


USE_REAL_LLM = False


class FakeLLMService:

    async def complete(
        self,
        prompt
    ):

        return LLMResponse(
            content="AI response",
            model="fake"
        )


def create_llm_service():

    if USE_REAL_LLM:

        provider = OllamaProvider(
            OllamaClient(),
            LLMConfig(
                model="llama3.2:3b"
            )
        )

        return LLMService(
            provider
        )


    return FakeLLMService()


@pytest.mark.asyncio
async def test_core_pipeline_uses_llm_handler():

    user_input = "hello"

    state = ConversationState(
        mode=ConversationMode.CHITCHAT
    )


    write_trace(
        "PIPELINE INPUT",
        {
            "user_input": user_input,
            "mode": state.mode,
            "llm_mode": (
                "real"
                if USE_REAL_LLM
                else "fake"
            )
        }
    )


    router = Router()


    llm_service = create_llm_service()


    router.register(
        ConversationMode.CHITCHAT,
        ChitchatHandler(
            llm_service
        )
    )


    core = CoreEngine(
        router
    )


    context = ContextBuilder().build(
        user_input=user_input,
        state=state
    )


    result = await core.process(
        context
    )


    write_trace(
        "PIPELINE OUTPUT",
        {
            "type": result.type,
            "content": result.content,
            "metadata": result.metadata
        }
    )


    assert result.type == "response"

    assert result.content

    assert result.metadata["model"]