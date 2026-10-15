import pytest

from core.execution.confirmation import (
    ConfirmationGate
)

from core.orchestration.models import (
    ReceptionResult
)


def test_confirmation_gate_detects_confirmation_requirement():

    gate = ConfirmationGate()


    result = ReceptionResult(
        mode="planner",
        requires_confirmation=True,
        reason="complex task detected"
    )


    assert gate.check(
        result
    ) is True

@pytest.mark.asyncio
async def test_confirmation_gate_allows_approved_execution():

    gate = ConfirmationGate()


    approved = await gate.confirm(
        True
    )


    assert approved is True

@pytest.mark.asyncio
async def test_confirmation_gate_blocks_rejected_execution():

    gate = ConfirmationGate()


    approved = await gate.confirm(
        False
    )


    assert approved is False