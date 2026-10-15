from core.agents.discovery import AgentDiscovery
from core.agents.registry import AgentRegistry


def test_registry_with_discovered_agents():

    discovery = AgentDiscovery()

    registry = AgentRegistry()


    for agent in discovery.discover():
        registry.register(agent)


    agents = registry.find_by_task(
        "get_weather"
    )


    assert len(agents) == 1

    assert (
        agents[0].metadata.name
        == "weather"
    )