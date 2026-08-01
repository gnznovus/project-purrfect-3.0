from core.agents.registry import AgentRegistry
from core.agents.models import AgentMetadata
from core.agents.base import SpecializedAgent


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


class FakeWeatherAgent(
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


def test_registry_discovers_agent_by_task():

    registry = AgentRegistry()


    registry.register(
        FakeCalendarAgent()
    )

    registry.register(
        FakeWeatherAgent()
    )


    agents = registry.find_by_task(
        "create_event"
    )


    assert len(agents) == 1

    assert agents[0].metadata.name == "calendar"