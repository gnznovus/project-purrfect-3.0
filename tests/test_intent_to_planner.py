import pytest

from core.intent.secretary import IntentSecretary
from core.intent.models import (
    Intent
)

from core.orchestration.planner import PlannerAgent
from core.orchestration.models import (
    ExecutionPlan
)


class FakeIntentExtractor:

    async def extract(
        self,
        user_input
    ):

        return Intent(
            type="chitchat",
            confidence=1.0
        )


class FakePlanner(PlannerAgent):

    async def create_plan(
        self,
        request_package
    ):

        return ExecutionPlan()


@pytest.mark.asyncio
async def test_intent_to_planner_pipeline():

    secretary = IntentSecretary(
        FakeIntentExtractor()
    )

    planner = FakePlanner()


    package = await secretary.process(
        "hello"
    )


    plan = await planner.create_plan(
        package
    )


    assert plan is not None

    assert isinstance(
        plan,
        ExecutionPlan
    )