from dataclasses import dataclass, field
from typing import Any

from core.context import RequestContext


@dataclass
class Intent:

    type: str

    entities: dict[str, Any] = field(
        default_factory=dict
    )

    confidence: float = 0.0

    context: str = ""


    def __post_init__(self):

        if self.type == "unknown" and not self.context:

            raise ValueError(
                "Unknown intent requires context"
            )


@dataclass
class IntentSet:

    intents: list[Intent] = field(
        default_factory=list
    )


@dataclass
class RequestPackage:

    intent_set: IntentSet

    context: RequestContext | None = None

    metadata: dict = field(
        default_factory=dict
    )