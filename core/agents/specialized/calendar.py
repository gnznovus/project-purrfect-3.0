from core.agents.base import SpecializedAgent

from core.agents.models import (
    AgentMetadata,
    AgentRequest,
    AgentResult
)


class CalendarAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="calendar",
        version="1.0",
        domain="calendar",
        description="Calendar management specialist",

        supported_tasks=[
            "create_event",
            "update_event",
            "delete_event",
            "list_events"
        ],

        input_requirements=[
            "title",
            "date"
        ],

        output_contract=[
            "result"
        ]
    )


    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        return AgentResult(
            domain=self.metadata.domain,
            result=f"{request.task} completed",
            confidence=1.0
        )