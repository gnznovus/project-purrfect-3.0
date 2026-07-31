import pytest

from core.context import RequestContext
from core.conversation.state import ConversationState
from core.state_update import StateUpdateType
from core.handlers.confirmation import ConfirmationHandler
from core.handlers.chitchat import ChitchatHandler
from core.llm.models import LLMResponse
from core.result import CoreResult

class FakeLLMService:

    async def complete(
        self,
        prompt
    ):

        return LLMResponse(
            content="hello from llm",
            model="fake"
        )

# --- Handlers --- #

@pytest.mark.asyncio
async def test_confirmation_handler_accepts():

    handler = ConfirmationHandler()


    context = RequestContext(
        request_id="confirm-001",
        user_input="yes",
        conversation_state=ConversationState()
    )


    result = await handler.handle(
        context
    )


    assert (
        result.state_updates[0].type
        == StateUpdateType.CONFIRM_PENDING_ACTION
    )

@pytest.mark.asyncio
async def test_chitchat_handler_uses_llm():

    handler = ChitchatHandler(
        FakeLLMService()
    )


    result = await handler.handle(
        type(
            "Context",
            (),
            {
                "user_input": "hello"
            }
        )()
    )


    assert isinstance(
        result,
        CoreResult
    )

    assert result.content == "hello from llm"

    assert result.metadata["model"] == "fake"