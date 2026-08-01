import pytest

from core.execution.engine import (
    ExecutionEngine
)

from core.agents.registry import (
    AgentRegistry
)

from core.agents.specialized.calendar import (
    CalendarAgent
)

from core.agents.specialized.travel import (
    TravelAgent
)

from core.orchestration.models import (
    ExecutionPlan,
    PlanStep
)

from tests.fakes.agents import (
    FailingWeatherAgent
)

from utils.trace import (
    write_section,
    write_trace
)


@pytest.mark.asyncio
async def test_execution_failure_pipeline_with_trace():

    write_section(
        "EXECUTION FAILURE PIPELINE"
    )


    plan = ExecutionPlan(
        steps=[
            PlanStep(
                capability="calendar",
                action="create_event",
                parameters={
                    "title": "Meeting"
                }
            ),

            PlanStep(
                capability="weather",
                action="get_weather",
                parameters={
                    "location": "Bangkok"
                }
            ),

            PlanStep(
                capability="travel",
                action="plan_trip",
                parameters={
                    "destination": "Japan"
                }
            )
        ]
    )


    registry = AgentRegistry()


    registry.register(
        CalendarAgent()
    )

    registry.register(
        FailingWeatherAgent()
    )

    registry.register(
        TravelAgent()
    )


    engine = ExecutionEngine(
        registry
    )


    executed_plan = await engine.execute(
        plan
    )


    for index, step in enumerate(
        executed_plan.steps,
        start=1
    ):

        write_trace(
            f"STEP #{index}",
            {
                "action": step.action,
                "status": step.status,
                "error": step.error
            }
        )


    assert (
        executed_plan.steps[0].status
        == "completed"
    )


    assert (
        executed_plan.steps[1].status
        == "failed"
    )


    assert (
        "weather service unavailable"
        in executed_plan.steps[1].error
    )


    assert (
        executed_plan.steps[2].status
        == "completed"
    )