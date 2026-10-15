import pytest

from core.execution.engine import (
    ExecutionEngine
)

from core.agents.registry import (
    AgentRegistry
)

from core.agents.models import (
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


class AlwaysFailWeatherAgent(
    WeatherAgent
):

    def __init__(self):
        self.calls = 0


    async def process(
        self,
        request: AgentRequest
    ):

        self.calls += 1

        raise Exception(
            "weather service unavailable"
        )


@pytest.mark.asyncio
async def test_execution_retry_exhausted_pipeline_with_trace():

    write_section(
        "EXECUTION RETRY EXHAUSTED PIPELINE"
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

    weather_agent = AlwaysFailWeatherAgent()


    registry = AgentRegistry()


    registry.register(
        CalendarAgent()
    )

    registry.register(
        weather_agent
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

    assert report.success is False
    assert weather_agent.calls == 3

    assert (
        report.steps[0].status
        == "completed"
    )


    assert (
        report.steps[1].status
        == "failed"
    )


    assert (
        report.steps[1].error
        == "weather service unavailable"
    )


    assert (
        report.steps[2].status
        == "completed"
    )