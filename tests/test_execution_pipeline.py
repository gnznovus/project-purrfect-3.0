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


def trace_result(
    result
):

    return {
        "domain": result.domain,
        "result": result.result,
        "confidence": result.confidence
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


    results = await engine.execute(
        plan
    )


    for index, result in enumerate(
        results,
        start=1
    ):

        write_trace(
            f"RESULT #{index}",
            trace_result(
                result
            )
        )


    assert len(results) == 3


    assert results[0].domain == "calendar"

    assert results[1].domain == "weather"

    assert results[2].domain == "travel"