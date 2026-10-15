from core.agents.discovery import (
    AgentDiscovery
)

from core.agents.registry import (
    AgentRegistry
)

from core.agents.snapshot import (
    CapabilitySnapshotBuilder
)

from utils.trace import (
    write_section,
    write_trace
)


def create_registry():

    registry = AgentRegistry()

    discovery = AgentDiscovery()


    for agent in discovery.discover():

        registry.register(
            agent
        )


    return registry


def test_capability_snapshot():

    write_section(
        "CAPABILITY SNAPSHOT"
    )


    registry = create_registry()


    builder = CapabilitySnapshotBuilder()


    snapshot = builder.build(
        registry
    )


    write_trace(
        "SNAPSHOT",
        {
            "capabilities": snapshot
        }
    )


    assert len(snapshot) > 0


    names = [
        item["name"]
        for item in snapshot
    ]


    assert "calendar" in names

    assert "weather" in names


def test_snapshot_contains_tasks():

    registry = create_registry()


    snapshot = CapabilitySnapshotBuilder().build(
        registry
    )


    weather = next(
        item
        for item in snapshot
        if item["name"] == "weather"
    )


    assert (
        "get_weather"
        in weather["supported_tasks"]
    )