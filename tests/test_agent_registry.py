from core.agents.registry import AgentRegistry

from core.agents.specialized.calendar import (
    CalendarAgent
)


def test_agent_registry_registers_agent():

    registry = AgentRegistry()


    agent = CalendarAgent()


    registry.register(
        agent
    )


    result = registry.get(
        "calendar"
    )


    assert result is agent