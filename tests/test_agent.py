import pytest

from core.agents.models import (
    AgentRequest,
    AgentResult
)

from core.agents.specialized.calendar import (
    CalendarAgent
)


@pytest.mark.asyncio
async def test_specialized_agent_processes_request():

    agent = CalendarAgent()


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

    assert result.result == "calendar action completed"

    assert result.confidence == 1.0