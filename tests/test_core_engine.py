import pytest

from core.context import RequestContext
from core.conversation.mode import ConversationMode
from core.conversation.state import ConversationState
from core.conversation.pending_transition import PendingTransition
from core.engine import CoreEngine
from core.router import Router
from core.result import CoreResult
from core.handler import Handler
from core.state_update import StateUpdate, StateUpdateType
from core.state_processor import StateUpdateProcessor

class FakeChitchatHandler(Handler):

    async def handle(self, context):
        return CoreResult(
            type="response",
            content="chitchat response"
        )


class FakePlannerHandler(Handler):

    async def handle(self, context):
        return CoreResult(
            type="response",
            content="planner response"
        )

class FakeErrorHandler(Handler):

    async def handle(self, context):
        raise RuntimeError("boom")

class FakeStateUpdateHandler:

    async def handle(self, context):

        return CoreResult(
            type="response",
            content="update requested",
            state_updates=[
                StateUpdate(
                    type=StateUpdateType.REQUEST_MODE_CHANGE,
                    value="planner"
                )
            ]
        )

class FakeStateManager:

    def __init__(self):
        self.received_updates = None


    async def apply(
        self,
        updates
    ):
        self.received_updates = updates

class FakeConfirmationHandler:

    def __init__(self):
        self.called = False


    async def handle(
        self,
        context
    ):
        self.called = True

        return CoreResult(
            type="response",
            content="confirmation response"
        )

class FakeInvalidHandler:

    async def handle(
        self,
        context
    ):
        return None

# --- Core Flow --- #

@pytest.mark.asyncio
async def test_core_routes_chitchat():

    router = Router()

    router.register(
        ConversationMode.CHITCHAT,
        FakeChitchatHandler()
    )

    router.register(
        ConversationMode.PLANNER,
        FakePlannerHandler()
    )

    core = CoreEngine(router)


    context = RequestContext(
        request_id="test-001",
        user_input="hello",
        conversation_state=ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    result = await core.process(context)


    assert result.content == "chitchat response"

@pytest.mark.asyncio
async def test_core_routes_planner():

    router = Router()

    router.register(
        ConversationMode.CHITCHAT,
        FakeChitchatHandler()
    )

    router.register(
        ConversationMode.PLANNER,
        FakePlannerHandler()
    )

    core = CoreEngine(router)

    context = RequestContext(
        request_id="test-002",
        user_input="plan trip",
        conversation_state=ConversationState(
            mode=ConversationMode.PLANNER
        )
    )

    result = await core.process(context)

    assert result.content == "planner response"

@pytest.mark.asyncio
async def test_core_handles_handler_error():

    router = Router()

    router.register(
        ConversationMode.CHITCHAT,
        FakeErrorHandler()
    )

    core = CoreEngine(router)

    context = RequestContext(
        request_id="test-error",
        user_input="hello",
        conversation_state=ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )

    result = await core.process(context)

    assert result.type == "error"

@pytest.mark.asyncio
async def test_core_returns_state_updates():

    router = Router()

    router.register(
        ConversationMode.CHITCHAT,
        FakeStateUpdateHandler()
    )

    core = CoreEngine(router)


    context = RequestContext(
        request_id="test-state-update",
        user_input="switch",
        conversation_state=ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    result = await core.process(context)


    assert len(result.state_updates) == 1

    assert (
        result.state_updates[0].type
        == StateUpdateType.REQUEST_MODE_CHANGE
    )

    assert result.state_updates[0].value == "planner"

@pytest.mark.asyncio
async def test_core_processes_state_updates():

    router = Router()

    router.register(
        ConversationMode.CHITCHAT,
        FakeStateUpdateHandler()
    )


    state_manager = FakeStateManager()

    processor = StateUpdateProcessor(
        state_manager
    )


    core = CoreEngine(
        router,
        state_processor=processor
    )


    context = RequestContext(
        request_id="test-state-processor",
        user_input="switch",
        conversation_state=ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    result = await core.process(context)


    assert result.state_updates

    assert (
        state_manager.received_updates
        == result.state_updates
    )

@pytest.mark.asyncio
async def test_core_routes_pending_confirmation():

    router = Router()

    router.register(
        ConversationMode.CHITCHAT,
        FakeChitchatHandler()
    )


    confirmation_handler = FakeConfirmationHandler()


    core = CoreEngine(
        router,
        confirmation_handler=confirmation_handler
    )


    state = ConversationState(
        mode=ConversationMode.CHITCHAT
    )


    state.pending_transition = PendingTransition(
        from_mode=ConversationMode.CHITCHAT,
        target_mode=ConversationMode.PLANNER,
        reason="planning request"
    )


    context = RequestContext(
        request_id="confirm-001",
        user_input="yes",
        conversation_state=state
    )


    result = await core.process(
        context
    )


    assert (
        result.content
        == "confirmation response"
    )

    assert (
        confirmation_handler.called
        is True
    )

@pytest.mark.asyncio
async def test_core_handles_invalid_handler_result():

    router = Router()

    router.register(
        ConversationMode.CHITCHAT,
        FakeInvalidHandler()
    )


    core = CoreEngine(
        router
    )


    context = RequestContext(
        request_id="invalid-result-001",
        user_input="hello",
        conversation_state=ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    result = await core.process(
        context
    )


    assert result.type == "error"

    assert (
        result.content
        == "An internal error occurred."
    )