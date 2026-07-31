import pytest

from core.context import RequestContext
from core.conversation.state import ConversationState
from core.state_update import StateUpdateType
from core.handlers.confirmation import ConfirmationHandler

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