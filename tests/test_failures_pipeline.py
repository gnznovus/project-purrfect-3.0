import pytest

from core.intent.secretary import (
    IntentSecretary
)
from core.intent.models import (
    Intent,
    IntentSet,
    RequestPackage
)
from core.intent.secretary import (
    IntentSecretary
)

from core.orchestration.models import (
    PlanStep,
    ExecutionPlan
)
from core.orchestration.response import (
    ResponseBuilder
)
from core.orchestration.reception import (
    ReceptionAgent
)
from core.orchestration.planner import (
    PlannerAgent
)

from core.agents.registry import (
    AgentRegistry
)
from core.agents.base import SpecializedAgent
from core.agents.models import (
    AgentMetadata,
    AgentRequest,
    AgentResult
)
from core.agents.specialized.calendar import (
    CalendarAgent
)
from core.agents.specialized.travel import (
    TravelAgent
)

from core.execution.engine import (
    ExecutionEngine
)
from core.execution.policy import (
    ExecutionPolicy
)

from utils.trace import (
    write_section,
    write_trace
)


class BrokenIntentExtractor:

    async def extract(
        self,
        user_input
    ):

        raise ValueError(
            "invalid LLM intent response"
        )

class UnknownIntentExtractor:

    async def extract(
        self,
        user_input
    ):

        return IntentSet(
            intents=[
                Intent(
                    type="summon_dragon",
                    confidence=1.0,
                    entities={}
                )
            ]
        )

class BrokenWeatherAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="weather",
        version="1.0",
        domain="weather",
        description="Broken weather specialist",

        supported_tasks=[
            "get_weather"
        ]
    )


    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        raise RuntimeError(
            "weather service unavailable"
        )

class MultiStepIntentExtractor:

    async def extract(
        self,
        user_input
    ):

        return IntentSet(
            intents=[
                Intent(
                    type="create_event",
                    confidence=1.0,
                    entities={
                        "date": "tomorrow"
                    }
                ),
                Intent(
                    type="get_weather",
                    confidence=1.0,
                    entities={}
                ),
                Intent(
                    type="plan_trip",
                    confidence=1.0,
                    entities={
                        "destination": "Chiang Mai"
                    }
                )
            ]
        )

class BrokenAgent(
    SpecializedAgent
):

    def __init__(
        self,
        name,
        task,
        error=None
    ):
        self.metadata = AgentMetadata(
            name=name,
            version="1.0",
            domain=name,
            description="test agent",
            supported_tasks=[
                task
            ]
        )

        self.error = error


    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        if self.error:
            raise RuntimeError(
                self.error
            )

        return AgentResult(
            domain=self.metadata.domain,
            result="completed",
            confidence=1.0
        )

class SuccessAgent(
    SpecializedAgent
):

    def __init__(
        self,
        domain,
        task
    ):
        self.metadata = AgentMetadata(
            name=f"{task}_agent",
            version="1.0",
            domain=domain,
            description=f"{task} specialist",
            supported_tasks=[
                task
            ]
        )


    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        return AgentResult(
            domain=self.metadata.domain,
            result=(
                f"{request.task} completed"
            ),
            confidence=1.0
        )

class RetryAgent(
    SpecializedAgent
):

    def __init__(
        self,
        name,
        task,
        fail_times=0
    ):
        self.attempts = 0
        self.fail_times = fail_times

        self.metadata = AgentMetadata(
            name=name,
            version="1.0",
            domain=name,
            description="retry test agent",
            supported_tasks=[
                task
            ]
        )


    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        self.attempts += 1


        if self.attempts <= self.fail_times:
            raise RuntimeError(
                "temporary failure"
            )


        return AgentResult(
            domain=self.metadata.domain,
            result="success",
            confidence=1.0
        )
    
class UnavailableAgent(
    SpecializedAgent
):

    def __init__(
        self,
        domain,
        task
    ):

        self.metadata = AgentMetadata(
            name=f"{task}_agent",
            version="1.0",
            domain=domain,
            description=f"{task} specialist",
            supported_tasks=[
                task
            ],
            available=False
        )


    async def process(
        self,
        request
    ):
        raise RuntimeError(
            "should never execute"
        )

@pytest.mark.asyncio
async def test_pipeline_stops_when_intent_extraction_fails():

    user_message = (
        "create a calendar event tomorrow"
    )


    write_section(
        "FAILURE PIPELINE - INTENT EXTRACTION"
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
        "RECEPTION",
        {
            "mode": reception_result.mode,
            "requires_confirmation": (
                reception_result.requires_confirmation
            )
        }
    )


    assert (
        reception_result.mode
        == "planner"
    )


    secretary = IntentSecretary(
        BrokenIntentExtractor()
    )


    try:

        await secretary.process(
            reception_result.context
        )


    except ValueError as error:

        write_trace(
            "SECRETARY FAILURE",
            {
                "error": str(error)
            }
        )


        write_trace(
            "PIPELINE RESULT",
            {
                "status": "stopped",
                "reason": "intent extraction failed"
            }
        )


        assert (
            str(error)
            == "invalid LLM intent response"
        )

        return


    pytest.fail(
        "Pipeline should have failed"
    )

@pytest.mark.asyncio
async def test_pipeline_stops_when_planner_receives_unknown_intent():

    user_message = (
        "summon a dragon"
    )


    write_section(
        "FAILURE PIPELINE - UNKNOWN INTENT"
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
        "RECEPTION",
        {
            "mode": reception_result.mode,
            "requires_confirmation": (
                reception_result.requires_confirmation
            )
        }
    )


    secretary = IntentSecretary(
        UnknownIntentExtractor()
    )


    intent_package = await secretary.process(
        reception_result.context
    )


    write_trace(
        "INTENTS",
        {
            "types": [
                intent.type
                for intent in (
                    intent_package.intent_set.intents
                )
            ]
        }
    )


    registry = AgentRegistry()


    planner = PlannerAgent(
        registry
    )


    with pytest.raises(
        Exception
    ) as error:

        await planner.create_plan(
            intent_package
        )


    write_trace(
        "PLANNER FAILURE",
        {
            "error": str(error.value)
        }
    )


    write_trace(
        "PIPELINE RESULT",
        {
            "status": "stopped",
            "reason": "planning failed"
        }
    )

@pytest.mark.asyncio
async def test_pipeline_handles_partial_execution_failure():

    user_message = (
        "create event, check weather, plan trip"
    )


    write_section(
        "FAILURE PIPELINE - EXECUTION FAILURE"
    )


    write_trace(
        "USER REQUEST",
        {
            "message": user_message
        }
    )


    secretary = IntentSecretary(
        MultiStepIntentExtractor()
    )


    intent_package = await secretary.process(
        {
            "user_message": user_message
        }
    )


    registry = AgentRegistry()


    registry.register(
        CalendarAgent()
    )

    registry.register(
        BrokenWeatherAgent()
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
            "steps": [
                step.action
                for step in plan.steps
            ]
        }
    )


    engine = ExecutionEngine(
        registry
    )


    report = await engine.execute(
        plan
    )


    write_trace(
        "EXECUTION REPORT",
        {
            "steps": [
                {
                    "action": step.action,
                    "status": step.status,
                    "error": step.error
                }
                for step in report.steps
            ]
        }
    )

@pytest.mark.asyncio
async def test_pipeline_skips_dependent_step_after_failure():

    write_section(
        "FAILURE PIPELINE - DEPENDENT JOB"
    )


    plan = ExecutionPlan(
        steps=[
            PlanStep(
                capability="resource",
                action="create_resource"
            ),

            PlanStep(
                capability="resource",
                action="process_resource",
                depends_on=[
                    "create_resource"
                ]
            ),

            PlanStep(
                capability="resource",
                action="publish_resource",
                depends_on=[
                    "process_resource"
                ]
            )
        ]
    )


    registry = AgentRegistry()


    registry.register(
        BrokenAgent(
            "creator",
            "create_resource"
        )
    )

    registry.register(
        BrokenAgent(
            "processor",
            "process_resource",
            error="processing failed"
        )
    )

    registry.register(
        BrokenAgent(
            "publisher",
            "publish_resource"
        )
    )


    engine = ExecutionEngine(
        registry
    )


    report = await engine.execute(
        plan
    )


    write_trace(
        "EXECUTION REPORT",
        {
            "steps": [
                {
                    "action": step.action,
                    "status": step.status,
                    "error": step.error
                }
                for step in report.steps
            ]
        }
    )


    assert report.steps[0].status == "completed"

    assert report.steps[1].status == "failed"

    assert report.steps[2].status == "skipped"

@pytest.mark.asyncio
async def test_pipeline_retries_failed_step_until_success():

    write_section(
        "FAILURE PIPELINE - RETRY SUCCESS"
    )


    agent = RetryAgent(
        "unstable",
        "unstable_task",
        fail_times=1
    )


    registry = AgentRegistry()

    registry.register(
        agent
    )


    engine = ExecutionEngine(
        registry,
        ExecutionPolicy(
            max_attempts=3
        )
    )


    plan = ExecutionPlan(
        steps=[
            PlanStep(
                capability="unstable",
                action="unstable_task"
            )
        ]
    )


    report = await engine.execute(
        plan
    )


    write_trace(
        "EXECUTION REPORT",
        {
            "attempts": agent.attempts,
            "status": report.steps[0].status
        }
    )


    assert agent.attempts == 2

    assert report.steps[0].status == "completed"

@pytest.mark.asyncio
async def test_pipeline_stops_after_retry_exhaustion():

    write_section(
        "FAILURE PIPELINE - RETRY EXHAUSTED"
    )


    agent = RetryAgent(
        "broken",
        "broken_task",
        fail_times=99
    )


    registry = AgentRegistry()

    registry.register(
        agent
    )


    engine = ExecutionEngine(
        registry,
        ExecutionPolicy(
            max_attempts=3
        )
    )


    plan = ExecutionPlan(
        steps=[
            PlanStep(
                capability="broken",
                action="broken_task"
            )
        ]
    )


    report = await engine.execute(
        plan
    )


    write_trace(
        "EXECUTION REPORT",
        {
            "attempts": agent.attempts,
            "status": report.steps[0].status,
            "error": report.steps[0].error
        }
    )


    assert agent.attempts == 3

    assert report.steps[0].status == "failed"

@pytest.mark.asyncio
async def test_pipeline_skips_dependency_after_retry_exhaustion():

    write_section(
        "FAILURE PIPELINE - RETRY DEPENDENCY"
    )


    first_agent = RetryAgent(
        "unstable",
        "create_resource",
        fail_times=99
    )


    second_agent = RetryAgent(
        "dependent",
        "process_resource"
    )


    registry = AgentRegistry()


    registry.register(
        first_agent
    )

    registry.register(
        second_agent
    )


    plan = ExecutionPlan(
        steps=[
            PlanStep(
                capability="unstable",
                action="create_resource"
            ),

            PlanStep(
                capability="dependent",
                action="process_resource",
                depends_on=[
                    "create_resource"
                ]
            )
        ]
    )


    engine = ExecutionEngine(
        registry,
        ExecutionPolicy(
            max_attempts=3
        )
    )


    report = await engine.execute(
        plan
    )


    write_trace(
        "EXECUTION REPORT",
        {
            "steps": [
                {
                    "action": step.action,
                    "status": step.status,
                    "error": step.error
                }
                for step in report.steps
            ],

            "dependent_attempts": (
                second_agent.attempts
            )
        }
    )


    assert report.steps[0].status == "failed"

    assert report.steps[1].status == "skipped"

    assert second_agent.attempts == 0

@pytest.mark.asyncio
async def test_planner_rejects_partial_invalid_intents():

    write_section(
        "PLANNER FAILURE - PARTIAL INVALID INTENT"
    )


    package = RequestPackage(
        intent_set=IntentSet(
            intents=[
                Intent(
                    type="create_event",
                    entities={}
                ),
                Intent(
                    type="summon_dragon",
                    entities={}
                )
            ]
        )
    )


    write_trace(
        "INTENTS",
        {
            "types": [
                intent.type
                for intent in package.intent_set.intents
            ]
        }
    )


    registry = AgentRegistry()


    registry.register(
        CalendarAgent()
    )


    planner = PlannerAgent(
        registry
    )


    try:

        await planner.create_plan(
            package
        )


    except ValueError as error:

        write_trace(
            "PLANNER FAILURE",
            {
                "error": str(error)
            }
        )


        write_trace(
            "PIPELINE RESULT",
            {
                "status": "stopped",
                "reason": "planning failed"
            }
        )


        assert (
            "Unknown capability: summon_dragon"
            in str(error)
        )

        return


    raise AssertionError(
        "Planner should reject invalid intent"
    )

@pytest.mark.asyncio
async def test_planner_rejects_empty_intents():

    write_section(
        "PLANNER FAILURE - EMPTY INTENT SET"
    )


    package = RequestPackage(
        intent_set=IntentSet(
            intents=[]
        )
    )


    write_trace(
        "INTENTS",
        {
            "types": [
                intent.type
                for intent in package.intent_set.intents
            ]
        }
    )


    registry = AgentRegistry()


    planner = PlannerAgent(
        registry
    )


    try:

        await planner.create_plan(
            package
        )


    except ValueError as error:

        write_trace(
            "PLANNER FAILURE",
            {
                "error": str(error)
            }
        )


        write_trace(
            "PIPELINE RESULT",
            {
                "status": "stopped",
                "reason": "planning failed"
            }
        )


        assert (
            str(error)
            == "No actionable intents"
        )

        return


    raise AssertionError(
        "Planner should reject empty intents"
    )

@pytest.mark.asyncio
async def test_pipeline_reports_partial_success():

    write_section(
        "FAILURE PIPELINE - PARTIAL SUCCESS REPORT"
    )


    plan = ExecutionPlan(
        steps=[
            PlanStep(
                capability="resource",
                action="create_resource"
            ),

            PlanStep(
                capability="resource",
                action="process_resource"
            ),

            PlanStep(
                capability="resource",
                action="publish_resource"
            )
        ]
    )


    registry = AgentRegistry()


    registry.register(
        SuccessAgent(
            "resource",
            "create_resource"
        )
    )


    registry.register(
        BrokenAgent(
            "resource",
            "process_resource",
            error="processing failed"
        )
    )


    registry.register(
        SuccessAgent(
            "resource",
            "publish_resource"
        )
    )


    engine = ExecutionEngine(
        registry
    )


    report = await engine.execute(
        plan
    )


    response = ResponseBuilder().build(
        report
    )


    write_trace(
        "FINAL RESPONSE",
        response
    )


    assert response["success"] is False


    assert len(
        response["results"]
    ) == 3


    assert (
        response["results"][0]["status"]
        == "completed"
    )


    assert (
        response["results"][1]["status"]
        == "failed"
    )


    assert (
        response["results"][1]["error"]
        == "processing failed"
    )


    assert (
        response["results"][2]["status"]
        == "completed"
    )

@pytest.mark.asyncio
async def test_planner_rejects_unavailable_capability():

    write_section(
        "PLANNER FAILURE - CAPABILITY UNAVAILABLE"
    )


    registry = AgentRegistry()

    registry.register(
        UnavailableAgent(
            "weather",
            "get_weather"
        )
    )


    planner = PlannerAgent(
        registry
    )


    package = RequestPackage(
        intent_set=IntentSet(
            intents=[
                Intent(
                    type="get_weather",
                    confidence=1.0
                )
            ]
        )
    )


    with pytest.raises(
        ValueError
    ) as error:

        await planner.create_plan(
            package
        )


    write_trace(
        "PLANNER FAILURE",
        {
            "error": str(
                error.value
            )
        }
    )


    write_trace(
        "PIPELINE RESULT",
        {
            "status": "stopped",
            "reason": "capability unavailable"
        }
    )


    assert (
        str(error.value)
        ==
        "Unknown capability: get_weather"
    )