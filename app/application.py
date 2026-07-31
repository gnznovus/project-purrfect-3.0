from core.context import RequestContext
from core.engine import CoreEngine
from core.conversation.manager import ConversationStateManager


class Application:

    def __init__(
        self,
        core: CoreEngine,
        conversation: ConversationStateManager
    ):
        self.core = core
        self.conversation = conversation


    async def handle_message(
        self,
        user_input: str
    ):

        state = self.conversation.get_state()

        context = RequestContext(
            request_id="generated-id",
            user_input=user_input,
            conversation_state=state
        )

        return await self.core.process(context)