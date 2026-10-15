from core.context import RequestContext
from core.engine import CoreEngine
from core.conversation.manager import ConversationStateManager
from core.context_builder import ContextBuilder


class Application:

    def __init__(
        self,
        core: CoreEngine,
        conversation: ConversationStateManager
    ):
        self.core = core
        self.conversation = conversation
        self.context_builder = ContextBuilder()


    async def handle_message(
        self,
        user_input: str
    ):

        state = self.conversation.get_state()
        pending_transition = state.pending_transition
        is_confirmation = pending_transition is not None

        context = self.context_builder.build(
            user_input,
            self.conversation.get_state()
        )

        result = await self.core.process(context)

        if (
            is_confirmation
            and result.content == "confirmed"
            and pending_transition.original_message
        ):
            return await self.handle_message(
                pending_transition.original_message
            )

        return result
