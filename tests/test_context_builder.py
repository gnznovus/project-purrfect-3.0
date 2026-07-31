from core.context_builder import ContextBuilder
from core.context import RequestContext
from core.conversation.state import ConversationState
from core.conversation.mode import ConversationMode


def test_context_builder_creates_request_context():

    builder = ContextBuilder()

    state = ConversationState(
        mode=ConversationMode.CHITCHAT
    )


    context = builder.build(
        user_input="hello",
        state=state
    )


    assert isinstance(
        context,
        RequestContext
    )

    assert context.user_input == "hello"

    assert context.conversation_state == state

    assert context.request_id is not None



def test_context_builder_preserves_conversation_state():

    builder = ContextBuilder()

    state = ConversationState(
        mode=ConversationMode.PLANNER
    )


    context = builder.build(
        user_input="plan my day",
        state=state
    )


    assert (
        context.conversation_state.mode
        == ConversationMode.PLANNER
    )