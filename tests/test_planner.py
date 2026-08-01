import pytest

from core.intent.models import (
    Intent,
    IntentSet,
    RequestPackage
)

from core.orchestration.models import (
    ExecutionPlan
)

from core.orchestration.planner import PlannerAgent


class FakePlanner(PlannerAgent):

    async def create_plan(
        self,
        request_package
    ):

        return ExecutionPlan()


@pytest.mark.asyncio
async def test_planner_creates_execution_plan():

    planner = FakePlanner()


    package = RequestPackage(
        intent_set=IntentSet(
            intents=[
                Intent(
                    type="chitchat",
                    confidence=1.0
                )
            ]
        )
    )


    result = await planner.create_plan(
        package
    )


    assert isinstance(
        result,
        ExecutionPlan
    )