from core.agents.registry import AgentRegistry

from core.agents.models import (
    AgentMetadata
)

from core.agents.base import (
    SpecializedAgent
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
        ],

        input_requirements=[
            "date",
            "title"
        ],

        output_contract=[
            "result",
            "missing_information"
        ],

        related_tools=[
            "calendar.create_event"
        ]
    )


def test_agent_registry_registers_agent():

    registry = AgentRegistry()


    agent = FakeCalendarAgent()


    registry.register(
        agent
    )


    result = registry.get(
        "calendar"
    )


    assert result is agent