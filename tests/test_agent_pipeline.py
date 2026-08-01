import pytest

from core.agents.registry import AgentRegistry

from core.agents.models import AgentRequest

from core.agents.specialized.calendar import CalendarAgent

from core.agents.specialized.weather import WeatherAgent

from core.agents.specialized.travel import TravelAgent

from utils.trace import (
    write_section,
    write_trace
)


@pytest.mark.asyncio
async def test_agent_pipeline_with_trace():

    user_task = "create_event"


    write_section(
        "PIPELINE INPUT"
    )

    write_trace(
        "USER REQUEST",
        {
            "task": user_task
        }
    )


    registry = AgentRegistry()


    agents = [
        CalendarAgent(),
        WeatherAgent(),
        TravelAgent()
    ]


    write_section(
        "AGENT REGISTRATION"
    )


    for agent in agents:

        registry.register(
            agent
        )

        write_trace(
            "AGENT REGISTERED",
            {
                "name": agent.metadata.name,
                "domain": agent.metadata.domain,
                "tasks": agent.metadata.supported_tasks
            }
        )


    write_section(
        "AGENT DISCOVERY"
    )


    matched_agents = registry.find_by_task(
        user_task
    )


    write_trace(
        "AGENTS MATCHED",
        {
            "requested_task": user_task,
            "matched_agents": [
                agent.metadata.name
                for agent in matched_agents
            ]
        }
    )


    assert len(matched_agents) == 1


    selected_agent = matched_agents[0]


    write_section(
        "AGENT EXECUTION"
    )


    result = await selected_agent.process(
        AgentRequest(
            task=user_task,
            context={
                "title": "Team Meeting",
                "date": "tomorrow"
            }
        )
    )


    write_trace(
        "AGENT RESULT",
        {
            "domain": result.domain,
            "result": result.result,
            "confidence": result.confidence
        }
    )


    write_section(
        "PIPELINE OUTPUT"
    )


    write_trace(
        "FINAL RESULT",
        {
            "domain": result.domain,
            "result": result.result
        }
    )


    assert result.domain == "calendar"

    assert result.result == "calendar action completed"