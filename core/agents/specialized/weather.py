from core.agents.base import SpecializedAgent

from core.agents.models import (
    AgentMetadata,
    AgentRequest,
    AgentResult
)


class WeatherAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="weather",
        version="1.0",
        domain="weather",
        description="Weather specialist",

        supported_tasks=[
            "get_weather"
        ]
    )


    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        return AgentResult(
            domain=self.metadata.domain,
            result="sunny",
            confidence=1.0
        )