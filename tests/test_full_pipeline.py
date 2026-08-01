import pytest

from core.orchestration.reception import (
    ReceptionAgent
)

from core.intent.secretary import (
    IntentSecretary
)

from core.intent.models import (
    Intent,
    IntentSet
)

from core.orchestration.planner import (
    PlannerAgent
)

from core.execution.engine import (
    ExecutionEngine
)

from core.orchestration.response import (
    ResponseBuilder
)

from core.agents.registry import (
    AgentRegistry
)

from core.agents.specialized.calendar import (
    CalendarAgent
)

from core.agents.specialized.weather import (
    WeatherAgent
)

from core.agents.specialized.travel import (
    TravelAgent
)

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

def trace_response(
    response
):

    return response

@pytest.mark.asyncio
async def test_full_orchestration_pipeline_with_trace():

    user_message = (
        "create a calendar event tomorrow, "
        "check the weather, "
        "and plan a trip"
    )


    write_section(
        "FULL PIPELINE"
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


    assert (
        reception_result.mode
        == "planner"
    )


    write_trace(
        "RECEPTION",
        {
            "mode": reception_result.mode
        }
    )


    secretary = IntentSecretary(
        FakeIntentExtractor()
    )


    intent_package = await secretary.process(
        reception_result.context
    )


    write_trace(
        "INTENTS",
        {
            "count": len(
                intent_package.intent_set.intents
            )
        }
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


    plan = await planner.create_plan(
        intent_package
    )


    write_trace(
        "PLAN",
        {
            "steps": len(plan.steps)
        }
    )


    engine = ExecutionEngine(
        registry
    )


    executed_plan = await engine.execute(
        plan
    )


    write_trace(
        "EXECUTION",
        {
            "completed": [
                step.action
                for step in executed_plan.steps
                if step.status == "completed"
            ]
        }
    )


    builder = ResponseBuilder()


    response = builder.build(
        executed_plan
    )


    write_trace(
        "FINAL RESPONSE",
        trace_response(
            response
        )
    )


    assert response["success"] is True


    assert len(
        response["results"]
    ) == 3


    assert (
        response["results"][0]["status"]
        == "completed"
    )