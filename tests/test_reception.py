import pytest

from core.orchestration.reception import (
    ReceptionAgent
)


@pytest.mark.asyncio
async def test_reception_handles_normal_conversation():

    agent = ReceptionAgent()

    result = await agent.process(
        "hello"
    )

    assert result.mode == "conversation"

    assert result.response == (
        "I can help with that."
    )


@pytest.mark.asyncio
async def test_reception_requests_planner():

    agent = ReceptionAgent()

    result = await agent.process(
        "create a meeting tomorrow"
    )

    assert result.mode == "planner"

    assert result.requires_confirmation is True