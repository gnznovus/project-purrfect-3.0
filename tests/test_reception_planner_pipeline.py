import pytest

from core.orchestration.reception import (
    ReceptionAgent
)

from core.orchestration.planner import (
    PlannerAgent
)

from utils.trace import (
    write_section,
    write_trace
)


@pytest.mark.asyncio
async def test_reception_to_planner_pipeline_with_trace():

    user_message = (
        "create a calendar event tomorrow"
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


    write_section(
        "RECEPTION DECISION"
    )


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
        "PLANNER TRANSITION"
    )


    write_trace(
        "PLANNER INPUT",
        {
            "context": reception_result.context
        }
    )


    planner = PlannerAgent()


    result = await planner.create_plan(
        reception_result.context
    )


    write_trace(
        "PLANNER RESULT",
        {
            "result": result
        }
    )


    assert result is not None