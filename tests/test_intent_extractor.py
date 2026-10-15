import pytest
from uuid import uuid4

from core.context import RequestContext
from core.conversation.state import ConversationState

from core.llm.config import LLMConfig
from core.llm.ollama.client import OllamaClient
from core.llm.ollama.provider import OllamaProvider

from core.intent.extractor import IntentExtractor
from core.intent.models import IntentSet
from core.intent.policy import IntentExtractionPolicy

from core.agents.discovery import AgentDiscovery
from core.agents.registry import AgentRegistry
from core.agents.snapshot import CapabilitySnapshotBuilder

from utils.trace import (
    write_section,
    write_trace
)


CAPABILITIES = True


def create_extractor() -> IntentExtractor:

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


def create_capability_snapshot():

    registry = AgentRegistry()

    discovery = AgentDiscovery()


    for agent in discovery.discover():

        registry.register(
            agent
        )


    return CapabilitySnapshotBuilder().build(
        registry
    )


def create_request_context(
    user_input: str,
    capabilities=None
) -> RequestContext:

    metadata = {}


    if capabilities is not None:

        metadata["capabilities"] = capabilities


    return RequestContext(
        request_id=str(
            uuid4()
        ),

        user_input=user_input,

        conversation_state=ConversationState(),

        metadata=metadata
    )


@pytest.mark.asyncio
async def test_intent_extractor():

    user_input = (
        "Schedule my meeting tomorrow book me a restaurant for dinner and check the weather."
    )


    write_section(
        "INTENT EXTRACTION"
    )


    capabilities = None


    if CAPABILITIES:

        capabilities = (
            create_capability_snapshot()
        )


    context = create_request_context(
        user_input,
        capabilities
    )


    extractor = create_extractor()


    system_prompt = (
        extractor.build_system_prompt(
            context
        )
    )


    write_trace(
        "PROMPT SOURCE",
        {
            "mode": (
                "dynamic_capabilities"
                if capabilities
                else "static_fallback"
            )
        }
    )


    write_trace(
        "SYSTEM PROMPT",
        {
            "prompt": system_prompt
        }
    )


    write_trace(
        "USER INPUT",
        {
            "message": user_input
        }
    )


    result = await extractor.extract(
        context
    )


    write_trace(
        "INTENT RESULT",
        {
            "count": len(
                result.intents
            ),
            "intents": [
                {
                    "type": intent.type,
                    "confidence": intent.confidence,
                    "entities": intent.entities
                }
                for intent in result.intents
            ]
        }
    )


    assert isinstance(
        result,
        IntentSet
    )


    assert len(
        result.intents
    ) == 3