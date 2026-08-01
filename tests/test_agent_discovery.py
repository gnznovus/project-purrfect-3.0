from core.agents.registry import AgentRegistry

from core.agents.specialized.calendar import (
    CalendarAgent
)

from core.agents.specialized.weather import (
    WeatherAgent
)

from core.agents.specialized.travel import (
    TravelAgent
)


def test_registry_discovers_agent_by_task():

    registry = AgentRegistry()


    registry.register(
        CalendarAgent()
    )

    registry.register(
        WeatherAgent()
    )


    agents = registry.find_by_task(
        "create_event"
    )


    assert len(agents) == 1

    assert (
        agents[0].metadata.name
        == "calendar"
    )

    assert (
        "create_event"
        in agents[0].metadata.supported_tasks
    )

def test_registry_discovers_multiple_domains():

    registry = AgentRegistry()

    registry.register(
        CalendarAgent()
    )

    registry.register(
        WeatherAgent()
    )

    registry.register(
        TravelAgent()
    )


    weather_agents = registry.find_by_task(
        "get_weather"
    )


    assert len(weather_agents) == 1

    assert (
        weather_agents[0].metadata.domain
        == "weather"
    )