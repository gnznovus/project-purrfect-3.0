import pytest

from core.context_builder import ContextBuilder
from core.engine import CoreEngine
from core.router import Router
from core.state_update import StateUpdate, StateUpdateType
from core.state_processor import StateUpdateProcessor
from core.result import CoreResult

from core.conversation.mode import ConversationMode
from core.conversation.state import ConversationState
from core.conversation.manager import ConversationStateManager


class FakeStateUpdateHandler:

    async def handle(
        self,
        context
    ):
        return CoreResult(
            type="response",
            content="task updated",
            state_updates=[
                StateUpdate(
                    type=StateUpdateType.SET_ACTIVE_TASK,
                    value="task-001"
                )
            ]
        )

@pytest.mark.asyncio
async def test_request_flows_through_core_pipeline():

    router = Router()

    router.register(
        ConversationMode.CHITCHAT,
        FakeStateUpdateHandler()
    )


    state_manager = ConversationStateManager(
        ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    processor = StateUpdateProcessor(
        state_manager
    )


    core = CoreEngine(
        router,
        state_processor=processor
    )


    builder = ContextBuilder()


    context = builder.build(
        user_input="switch task",
        state=state_manager.get_state()
    )


    result = await core.process(
        context
    )


    assert result.type == "response"

    assert result.state_updates


    assert (
        state_manager.get_state()
        .active_task_id
        == "task-001"
    )