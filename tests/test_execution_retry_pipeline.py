import pytest

from core.execution.engine import (
    ExecutionEngine
)

from core.agents.registry import (
    AgentRegistry
)

from core.agents.models import (
    AgentResult,
    AgentRequest
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


class FlakyWeatherAgent(
    WeatherAgent
):

    def __init__(self):

        self.calls = 0


    async def process(
        self,
        request: AgentRequest
    ):

        self.calls += 1


        write_trace(
            "WEATHER ATTEMPT",
            {
                "attempt": self.calls
            }
        )


        if self.calls == 1:

            raise Exception(
                "temporary failure"
            )


        return AgentResult(
            domain="weather",
            result="sunny",
            confidence=1.0
        )


@pytest.mark.asyncio
async def test_execution_retry_pipeline_with_trace():

    write_section(
        "EXECUTION RETRY PIPELINE"
    )


    plan = ExecutionPlan(
        steps=[
            PlanStep(
                capability="calendar",
                action="create_event",
                parameters={
                    "title": "Meeting",
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


    registry = AgentRegistry()


    registry.register(
        CalendarAgent()
    )

    registry.register(
        FlakyWeatherAgent()
    )

    registry.register(
        TravelAgent()
    )


    engine = ExecutionEngine(
        registry
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
            {
                "action": step.action,
                "status": step.status,
                "error": step.error
            }
        )

    assert report.success is True

    assert (
        report.steps[0].status
        == "completed"
    )


    assert (
        report.steps[1].status
        == "completed"
    )


    assert (
        report.steps[1].result.result
        == "sunny"
    )


    assert (
        report.steps[2].status
        == "completed"
    )