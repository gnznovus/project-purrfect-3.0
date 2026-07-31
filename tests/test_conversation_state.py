import pytest

from core.conversation.mode import ConversationMode
from core.conversation.state import ConversationState
from core.state_update import StateUpdate, StateUpdateType
from core.conversation.manager import ConversationStateManager
from core.conversation.pending_transition import PendingTransition

# --- State Managment --- #

@pytest.mark.asyncio
async def test_state_manager_updates_active_task():

    manager = ConversationStateManager()


    await manager.apply(
        [
            StateUpdate(
                type=StateUpdateType.SET_ACTIVE_TASK,
                value="trip_planning"
            )
        ]
    )


    state = manager.get_state()


    assert state.active_task_id == "trip_planning"

def test_state_manager_validates_mode_transition():

    manager = ConversationStateManager(
        ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    assert (
        manager.can_transition(
            ConversationMode.PLANNER
        )
        is True
    )


    manager.state.mode = ConversationMode.PLANNER


    assert (
        manager.can_transition(
            ConversationMode.CHITCHAT
        )
        is True
    )

def test_state_contains_pending_transition():

    state = ConversationState(
        mode=ConversationMode.CHITCHAT,
        pending_transition=PendingTransition(
            from_mode=ConversationMode.CHITCHAT,
            target_mode=ConversationMode.PLANNER,
            reason="trip planning"
        )
    )


    assert state.pending_transition is not None

    assert (
        state.pending_transition.target_mode
        == ConversationMode.PLANNER
    )

    assert (
        state.pending_transition.reason
        == "trip planning"
    )

def test_state_manager_requests_transition():

    manager = ConversationStateManager(
        ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    manager.request_transition(
        ConversationMode.PLANNER,
        "trip planning"
    )


    pending = manager.get_state().pending_transition


    assert pending is not None

    assert (
        pending.from_mode
        == ConversationMode.CHITCHAT
    )

    assert (
        pending.target_mode
        == ConversationMode.PLANNER
    )

    assert (
        pending.reason
        == "trip planning"
    )

    assert (
        manager.get_state().mode
        == ConversationMode.CHITCHAT
    )

def test_state_manager_confirms_transition():

    manager = ConversationStateManager(
        ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    manager.request_transition(
        ConversationMode.PLANNER,
        "trip planning"
    )


    manager.confirm_transition()


    assert (
        manager.get_state().mode
        == ConversationMode.PLANNER
    )

    assert (
        manager.get_state().pending_transition
        is None
    )

def test_state_manager_rejects_transition():

    manager = ConversationStateManager(
        ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    manager.request_transition(
        ConversationMode.PLANNER,
        "trip planning"
    )


    manager.reject_transition()


    assert (
        manager.get_state().mode
        == ConversationMode.CHITCHAT
    )

    assert (
        manager.get_state().pending_transition
        is None
    )

def test_state_manager_requests_mode_change_from_update():

    manager = ConversationStateManager(
        ConversationState(
            mode=ConversationMode.CHITCHAT
        )
    )


    manager_update = StateUpdate(
        type=StateUpdateType.REQUEST_MODE_CHANGE,
        value="planner",
        reason="trip planning"
    )


    import asyncio

    asyncio.run(
        manager.apply(
            [manager_update]
        )
    )


    state = manager.get_state()


    assert (
        state.mode
        == ConversationMode.CHITCHAT
    )


    assert (
        state.pending_transition is not None
    )


    assert (
        state.pending_transition.target_mode
        == ConversationMode.PLANNER
    )


    assert (
        state.pending_transition.reason
        == "trip planning"
    )