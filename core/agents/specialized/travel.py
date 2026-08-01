from core.agents.base import SpecializedAgent

from core.agents.models import (
    AgentMetadata,
    AgentRequest,
    AgentResult
)


class TravelAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="travel",
        version="1.0",
        domain="travel",
        description="Travel planning specialist",

        supported_tasks=[
            "plan_trip",
            "build_itinerary"
        ],

        input_requirements=[
            "destination",
            "date"
        ],

        output_contract=[
            "itinerary"
        ]
    )


    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        return AgentResult(
            domain=self.metadata.domain,
            result="trip planned",
            confidence=1.0
        )