from dataclasses import dataclass

from core.agents.discovery import AgentDiscovery
from core.agents.registry import AgentRegistry
from core.conversation.manager import ConversationStateManager
from core.engine import CoreEngine
from core.handlers.chitchat import ChitchatHandler
from core.handlers.confirmation import ConfirmationHandler
from core.handlers.planner import PlannerHandler
from core.intent.extractor import IntentExtractor
from core.intent.policy import IntentExtractionPolicy
from core.intent.secretary import IntentSecretary
from core.llm.config import LLMConfig
from core.llm.ollama.client import OllamaClient
from core.llm.ollama.provider import OllamaProvider
from core.llm.service import LLMService
from core.router import Router
from core.state_processor import StateUpdateProcessor
from core.memory.working import WorkingMemory
from core.orchestration.planner import PlannerAgent
from core.orchestration.clarification import ClarificationExtractor
from core.orchestration.response import ResponseBuilder
from core.agents.snapshot import CapabilitySnapshotBuilder

from app.application import Application


@dataclass
class ApplicationComponents:
    application: Application
    conversation: ConversationStateManager
    registry: AgentRegistry
    llm_service: LLMService


def build_application(
    llm_config: LLMConfig | None = None,
    ollama_url: str = "http://localhost:11434"
) -> ApplicationComponents:
    config = llm_config or LLMConfig(model="llama3.2:3b")

    provider = OllamaProvider(
        OllamaClient(base_url=ollama_url),
        config
    )
    llm_service = LLMService(provider)

    registry = AgentRegistry()
    for agent in AgentDiscovery().discover():
        registry.register(agent)

    capability_snapshot = CapabilitySnapshotBuilder().build(
        registry
    )
    secretary = IntentSecretary(
        IntentExtractor(
            provider,
            IntentExtractionPolicy()
        ),
        capability_snapshot
    )
    working_memory = WorkingMemory()

    conversation = ConversationStateManager()
    state_processor = StateUpdateProcessor(conversation)

    router = Router()
    router.register(
        "chitchat",
        ChitchatHandler(llm_service)
    )
    router.register(
        "planner",
        PlannerHandler(
            secretary=secretary,
            planner=PlannerAgent(registry),
            working_memory=working_memory,
            capability_snapshot=capability_snapshot,
            clarification_extractor=ClarificationExtractor(provider),
            response_builder=ResponseBuilder(llm_service)
        )
    )

    core = CoreEngine(
        router=router,
        state_processor=state_processor,
        confirmation_handler=ConfirmationHandler()
    )

    application = Application(
        core=core,
        conversation=conversation
    )

    return ApplicationComponents(
        application=application,
        conversation=conversation,
        registry=registry,
        llm_service=llm_service
    )
