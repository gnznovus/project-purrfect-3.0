from dataclasses import dataclass

from .mode import ConversationMode
from .pending_transition import PendingTransition


@dataclass
class ConversationState:

    mode: ConversationMode = ConversationMode.CHITCHAT

    active_task_id: str | None = None

    pending_transition: PendingTransition | None = None