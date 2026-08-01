import pytest

from core.agents.registry import AgentRegistry

from core.agents.specialized.calendar import CalendarAgent
from core.agents.specialized.weather import WeatherAgent
from core.agents.specialized.travel import TravelAgent


from core.intent.models import (
    Intent,
    IntentSet
)

from core.intent.secretary import IntentSecretary


from core.orchestration.models import (
    ExecutionPlan
)

from core.orchestration.planner import PlannerAgent
from core.orchestration.reception import ReceptionAgent

from utils.trace import (
    write_section,
    write_trace
)

class FakeIntentExtractor:

    async def extract(
        self,
        user_input
    ):

        return IntentSet(
            intents=[
                Intent(
                    type="create_event",
                    confidence=1.0
                ),
                Intent(
                    type="get_weather",
                    confidence=0.95
                ),
                Intent(
                    type="plan_trip",
                    confidence=0.90
                )
            ]
        )


def trace_request_package(
    package
):

    return {
        "intents": [
            {
                "type": intent.type,
                "confidence": intent.confidence
            }
            for intent in package.intent_set.intents
        ],
        "metadata": package.metadata
    }


@pytest.mark.asyncio
async def test_reception_intent_planner_pipeline_with_trace():

    user_message = (
        "create a calendar event tomorrow, "
        "check the weather, "
        "and plan a trip"
    )

    write_section(
        "RECEPTION PIPELINE"
    )

    write_trace(
        "USER REQUEST",
        {
            "message": user_message
        }
    )


    reception = ReceptionAgent()


    reception_result = await reception.process(
        user_message
    )


    write_trace(
        "RECEPTION RESULT",
        {
            "mode": reception_result.mode,
            "requires_confirmation": (
                reception_result.requires_confirmation
            ),
            "reason": reception_result.reason,
            "context": reception_result.context
        }
    )


    assert reception_result.mode == "planner"


    write_section(
        "INTENT PIPELINE"
    )


    secretary = IntentSecretary(
        FakeIntentExtractor()
    )


    intent_package = await secretary.process(
        reception_result.context
    )


    write_trace(
        "INTENT RESULT",
        trace_request_package(
            intent_package
        )
    )


    assert len(
        intent_package.intent_set.intents
    ) == 3


    assert (
        intent_package.intent_set.intents[0].type
        == "create_event"
    )

    assert (
        intent_package.intent_set.intents[1].type
        == "get_weather"
    )

    assert (
        intent_package.intent_set.intents[2].type
        == "plan_trip"
    )

    write_section(
        "PLANNER PIPELINE"
    )


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


    planner = PlannerAgent(
        registry
    )


    write_trace(
        "PLANNER INPUT",
        trace_request_package(
            intent_package
        )
    )


    plan = await planner.create_plan(
        intent_package
    )


    write_trace(
        "PLAN CREATED",
        {
            "steps": len(plan.steps)
        }
    )


    for index, step in enumerate(
        plan.steps,
        start=1
    ):

        write_trace(
            f"STEP #{index}",
            {
                "capability": step.capability,
                "action": step.action,
                "parameters": step.parameters
            }
        )


    assert isinstance(
        plan,
        ExecutionPlan
    )

    assert len(plan.steps) == 3

    assert plan.steps[0].capability == "calendar"

    assert plan.steps[0].action == "create_event"

    assert plan.steps[1].capability == "weather"

    assert plan.steps[1].action == "get_weather"

    assert plan.steps[2].capability == "travel"

    assert plan.steps[2].action == "plan_trip"