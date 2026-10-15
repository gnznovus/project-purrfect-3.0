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

from core.agents.specialized.weather import (
    WeatherAgent
)

from core.agents.specialized.travel import (
    TravelAgent
)

from core.orchestration.models import (
    ExecutionPlan,
    PlanStep
)

from utils.trace import (
    write_section,
    write_trace
)


def trace_step(
    step
):

    return {
        "capability": step.capability,
        "action": step.action,
        "status": step.status,
        "result": (
            step.result.result
            if step.result
            else None
        ),
        "error": step.error
    }


@pytest.mark.asyncio
async def test_execution_pipeline_with_trace():

    write_section(
        "EXECUTION PIPELINE"
    )


    plan = ExecutionPlan(
        steps=[
            PlanStep(
                capability="calendar",
                action="create_event",
                parameters={
                    "title": "Team Meeting",
                    "date": "tomorrow"
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


    write_trace(
        "EXECUTION PLAN",
        {
            "steps": len(plan.steps)
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


    engine = ExecutionEngine(
        registry
    )


    write_section(
        "EXECUTION RESULT"
    )


    report = await engine.execute(
        plan
    )


    for index, step in enumerate(
        report.steps,
        start=1
    ):

        write_trace(
            f"STEP #{index}",
            trace_step(
                step
            )
        )

    assert report.success is True

    assert len(
        report.steps
    ) == 3


    assert (
        report.steps[0].status
        == "completed"
    )

    assert (
        report.steps[0].result.domain
        == "calendar"
    )


    assert (
        report.steps[1].status
        == "completed"
    )

    assert (
        report.steps[1].result.domain
        == "weather"
    )


    assert (
        report.steps[2].status
        == "completed"
    )

    assert (
        report.steps[2].result.domain
        == "travel"
    )