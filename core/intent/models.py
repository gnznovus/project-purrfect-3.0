from dataclasses import dataclass, field


@dataclass
class Intent:

    type: str

    entities: dict = field(
        default_factory=dict
    )

    confidence: float = 0.0


@dataclass
class IntentSet:

    intents: list[Intent] = field(
        default_factory=list
    )


@dataclass
class RequestPackage:

    intent_set: IntentSet

    metadata: dict = field(
        default_factory=dict
    )