from core.agents.models import (
    AgentMetadata,
    AgentRequest,
    AgentResult
)


class SpecializedAgent:

    metadata: AgentMetadata


    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        raise NotImplementedError