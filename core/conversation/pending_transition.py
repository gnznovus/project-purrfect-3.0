from dataclasses import dataclass

from .mode import ConversationMode


@dataclass
class PendingTransition:

    from_mode: ConversationMode

    target_mode: ConversationMode

    reason: str