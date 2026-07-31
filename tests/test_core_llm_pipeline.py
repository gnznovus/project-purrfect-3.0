import pytest

from core.engine import CoreEngine
from core.router import Router
from core.result import CoreResult

from core.context_builder import ContextBuilder

from core.conversation.mode import ConversationMode
from core.conversation.state import ConversationState

from core.handlers.chitchat import ChitchatHandler


class FakeLLMService:

    async def complete(
        self,
        prompt
    ):

        from core.llm.models import LLMResponse

        return LLMResponse(
            content="AI response",
            model="fake"
        )


@pytest.mark.asyncio
async def test_core_pipeline_uses_llm_handler():

    router = Router()


    router.register(
        ConversationMode.CHITCHAT,
        ChitchatHandler(
            FakeLLMService()
        )
    )


    core = CoreEngine(
        router
    )


    builder = ContextBuilder()


    context = builder.build(
        user_input="hello",
        state=ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    result = await core.process(
        context
    )


    assert result.type == "response"

    assert result.content == "AI response"

    assert result.metadata["model"] == "fake"