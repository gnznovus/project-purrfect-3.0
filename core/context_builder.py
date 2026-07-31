from uuid import uuid4

from .context import RequestContext
from .conversation.state import ConversationState


class ContextBuilder:

    def build(
        self,
        user_input: str,
        state: ConversationState
    ) -> RequestContext:

        return RequestContext(
            request_id=str(uuid4()),
            user_input=user_input,
            conversation_state=state
        )