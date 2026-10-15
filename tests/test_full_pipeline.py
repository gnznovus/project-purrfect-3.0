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

from core.intent.extractor import (
    IntentExtractor
)

from core.intent.policy import (
    IntentExtractionPolicy
)

from core.orchestration.planner import (
    PlannerAgent
)

from core.orchestration.models import (
    ClarificationResponse
)

from core.execution.confirmation import (
    ConfirmationGate
)

from core.execution.engine import (
    ExecutionEngine
)

from core.orchestration.response import (
    ResponseBuilder
)

from core.agents.discovery import (
    AgentDiscovery
)

from core.agents.registry import (
    AgentRegistry
)

from core.agents.snapshot import (
    CapabilitySnapshotBuilder
)

from core.llm.ollama.client import (
    OllamaClient
)

from core.llm.ollama.provider import (
    OllamaProvider
)

from core.llm.config import (
    LLMConfig
)

from utils.trace import (
    write_section,
    write_trace
)

from core.memory.working import (
    WorkingMemory
)

APPROVAL = True

FAKE_EXTRACTOR = True


class FakeIntentExtractor:

    async def extract(
        self,
        context
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


def create_intent_extractor():

    if FAKE_EXTRACTOR:

        return FakeIntentExtractor()


    provider = OllamaProvider(
        OllamaClient(),
        LLMConfig(
            model="llama3.2:3b",
            temperature=0.0
        )
    )


    return IntentExtractor(
        provider,
        IntentExtractionPolicy()
    )


@pytest.mark.asyncio
async def test_full_orchestration_pipeline_with_trace():

    user_message = (
        "Help me organize my plans for tomorrow. "
        "Set something up for the afternoon, "
        "tell me if I need an umbrella, "
        "prepare something for my weekend, "
        "send a message to my friend about it, "
        "and maybe find something interesting nearby."
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

    assert reception_result.context is not None


    write_trace(
        "RECEPTION",
        {
            "mode": reception_result.mode,
            "requires_confirmation": (
                reception_result.requires_confirmation
            )
        }
    )


    #
    # Agent Discovery
    #

    discovery = AgentDiscovery()


    agents = discovery.discover()


    write_trace(
        "DISCOVERED AGENTS",
        {
            "agents": [
                agent.metadata.name
                for agent in agents
            ]
        }
    )


    #
    # Registry Bootstrap
    #

    registry = AgentRegistry()


    for agent in agents:

        registry.register(
            agent
        )


    write_trace(
        "REGISTRY",
        {
            "agents": [
                agent.metadata.name
                for agent in registry.list_agents()
            ]
        }
    )


    #
    # Capability Snapshot
    #

    snapshot_builder = CapabilitySnapshotBuilder()


    capability_snapshot = (
        snapshot_builder.build(
            registry
        )
    )


    write_trace(
        "CAPABILITY SNAPSHOT",
        {
            "capabilities": capability_snapshot
        }
    )


    #
    # Intent Extraction + Normalization
    #

    secretary = IntentSecretary(
        create_intent_extractor(),
        capability_snapshot
    )


    intent_package = await secretary.process(
        reception_result.context
    )


    write_trace(
        "INTENTS",
        {
            "count": len(
                intent_package.intent_set.intents
            ),

            "intents": [
                {
                    "type": intent.type,

                    "confidence": (
                        intent.confidence
                    ),

                    "entities": (
                        intent.entities
                    ),

                    "context": (
                        intent.context
                    )
                }

                for intent in (
                    intent_package.intent_set.intents
                )
            ]
        }
    )


    #
    # Planning
    #

    planner = PlannerAgent(
        registry
    )


    planner_result = await planner.create_plan(
        intent_package
    )

    write_trace(
        "PLANNER",
        {
            "status": planner_result.status
        }
    )


    if planner_result.plan:

        write_trace(
            "PARTIAL PLAN",
            {
                "steps": [
                    {
                        "action": step.action,
                        "capability": step.capability,
                        "status": step.status
                    }
                    for step in planner_result.plan.steps
                ]
            }
        )

    working_memory = WorkingMemory()

    if planner_result.status == "needs_clarification":

        working_memory.store(
            planner_result.pending_task
        )

        write_trace(
            "CLARIFICATION",
            {
                "reason": (
                    planner_result.clarification.reason
                ),
                "questions": (
                    planner_result.clarification.questions
                ),
                "intent_indexes": (
                    planner_result.clarification.intent_indexes
                )
            }
        )

        write_trace(
            "WORKING MEMORY",
            {
                "stored": working_memory.has_pending()
            }
        )

        return

    plan = planner_result.plan

    write_trace(
        "PLAN",
        {
            "steps": len(plan.steps)
        }
    )


    #
    # Confirmation
    #

    confirmation_gate = ConfirmationGate()


    requires_confirmation = (
        confirmation_gate.check(
            reception_result
        )
    )


    write_trace(
        "CONFIRMATION REQUIRED",
        {
            "required": requires_confirmation
        }
    )


    approved = await confirmation_gate.confirm(
        APPROVAL
    )


    write_trace(
        "CONFIRMATION RESULT",
        {
            "approved": approved
        }
    )


    if not approved:

        write_trace(
            "PIPELINE RESULT",
            {
                "status": "cancelled"
            }
        )

        assert approved is False

        return


    #
    # Execution
    #

    engine = ExecutionEngine(
        registry
    )


    report = await engine.execute(
        plan
    )


    write_trace(
        "EXECUTION",
        {
            "completed": [
                step.action
                for step in report.steps
                if step.status == "completed"
            ]
        }
    )


    #
    # Response
    #

    builder = ResponseBuilder()


    response = builder.build(
        report
    )


    write_trace(
        "FINAL RESPONSE",
        response
    )


    # assert response["success"] is True

    # assert len(
    #     response["results"]
    # ) == 3

    # assert (
    #     response["results"][0]["status"]
    #     == "completed"
    # )

@pytest.mark.asyncio
async def test_planner_resume_after_clarification():

    user_message = (
        "Help me organize my plans for tomorrow. "
        "Set something up for the afternoon, "
        "tell me if I need an umbrella, "
        "prepare something for my weekend, "
        "send a message to my friend about it, "
        "and maybe find something interesting nearby."
    )


    reception = ReceptionAgent()

    reception_result = await reception.process(
        user_message
    )


    registry = AgentRegistry()

    for agent in AgentDiscovery().discover():

        registry.register(
            agent
        )


    secretary = IntentSecretary(
        create_intent_extractor(),
        CapabilitySnapshotBuilder().build(
            registry
        )
    )


    intent_package = await secretary.process(
        reception_result.context
    )


    planner = PlannerAgent(
        registry
    )


    #
    # First planning attempt
    #

    first_result = await planner.create_plan(
        intent_package
    )


    assert (
        first_result.status
        == "needs_clarification"
    )


    assert (
        first_result.pending_task
        is not None
    )


    #
    # Simulated user answers
    #

    clarification_response = ClarificationResponse(
        answers={
            2: {
                "type": "plan_trip",
                "entities": {
                    "activity": "picnic"
                },
                "context": (
                    "Prepare a picnic "
                    "for weekend"
                )
            },

            3: {
                "type": "send_email",
                "entities": {
                    "recipient": "friend"
                },
                "context": (
                    "Send message "
                    "to friend"
                )
            },

            4: {
                "type": "web_search",
                "entities": {
                    "query": (
                        "interesting places nearby"
                    )
                },
                "context": (
                    "Find something "
                    "interesting nearby"
                )
            }
        }
    )


    #
    # Resume
    #

    resumed_result = await planner.resume(
        first_result.pending_task,
        clarification_response
    )


    assert (
        resumed_result.status
        == "ready"
    )


    assert (
        resumed_result.plan
        is not None
    )


    assert len(
        resumed_result.plan.steps
    ) == 5