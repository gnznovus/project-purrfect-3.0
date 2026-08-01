import pytest

from core.agents.base import SpecializedAgent

from core.agents.models import (
    AgentMetadata,
    AgentRequest,
    AgentResult
)


class FakeCalendarAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="calendar",
        version="1.0",
        domain="calendar",
        description="Calendar specialist",
        supported_tasks=[
            "create_event"
        ]
    )


    async def process(
        self,
        request: AgentRequest
    ):

        return AgentResult(
            domain=self.metadata.domain,
            result="event created",
            confidence=1.0
        )


@pytest.mark.asyncio
async def test_specialized_agent_processes_request():

    agent = FakeCalendarAgent()


    request = AgentRequest(
        task="create_event",
        context={
            "title": "Meeting"
        }
    )


    result = await agent.process(
        request
    )


    assert isinstance(
        result,
        AgentResult
    )

    assert result.domain == "calendar"

    assert result.result == "event created"

    assert result.confidence == 1.0