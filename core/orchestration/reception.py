from core.orchestration.models import (
    ReceptionResult
)

from core.context import (
    RequestContext
)

from core.conversation.state import (
    ConversationState
)

import uuid


class ReceptionAgent:

    async def process(
        self,
        message: str
    ) -> ReceptionResult:

        if self._requires_planner(
            message
        ):

            return ReceptionResult(
                mode="planner",
                requires_confirmation=True,
                reason="complex task detected",
                context=RequestContext(
                    request_id=str(
                        uuid.uuid4()
                    ),
                    user_input=message,
                    conversation_state=ConversationState()
                )
            )


        return ReceptionResult(
            mode="conversation",
            response=self._respond(
                message
            )
        )


    def _requires_planner(
        self,
        message: str
    ) -> bool:

        keywords = [
            "create",
            "plan",
            "schedule",
            "organize"
        ]

        return any(
            keyword in message.lower()
            for keyword in keywords
        )


    def _respond(
        self,
        message: str
    ) -> str:

        return (
            "I can help with that."
        )