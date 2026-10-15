from core.agents.discovery import (
    AgentDiscovery
)

from core.agents.base import (
    SpecializedAgent
)

from utils.trace import (
    write_section,
    write_trace
)


def test_agent_discovery():

    write_section(
        "AGENT DISCOVERY - RAW AGENTS"
    )


    discovery = AgentDiscovery()


    agents = discovery.discover()


    write_trace(
        "DISCOVERED AGENT OBJECTS",
        {
            "agents": [
                {
                    "class": agent.__class__.__name__,
                    "module": agent.__class__.__module__,
                    "object_type": str(
                        type(agent)
                    ),
                    "metadata": str(
                        agent.metadata
                    )
                }
                for agent in agents
            ]
        }
    )


    assert len(
        agents
    ) > 0


    assert all(
        isinstance(
            agent,
            SpecializedAgent
        )
        for agent in agents
    )


def test_discovered_agent_support_tasks():

    discovery = AgentDiscovery()


    agents = discovery.discover()


    calendar = next(
        agent
        for agent in agents
        if agent.metadata.name == "calendar"
    )


    assert (
        "create_event"
        in calendar.metadata.supported_tasks
    )