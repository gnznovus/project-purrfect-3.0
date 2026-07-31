from dataclasses import dataclass, field
from typing import Any
from .conversation.state import ConversationState


@dataclass
class RequestContext:

    request_id: str

    user_input: str

    conversation_state: ConversationState

    memory_context: dict[str, Any] = field(
        default_factory=dict
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )