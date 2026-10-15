from dataclasses import dataclass, field

from core.context import (
    RequestContext
)

from core.intent.models import (
    RequestPackage
)


@dataclass
class PlanStep:

    step_type: str = "execute"

    capability: str | None = None

    action: str | None = None

    parameters: dict = field(
        default_factory=dict
    )

    context: str | None = None

    depends_on: list[str] = field(
        default_factory=list
    )

    status: str = "pending"

    result: object | None = None

    error: str | None = None

    reason: str | None = None

@dataclass
class ClarificationRequest:

    reason: str

    questions: list[str] = field(
        default_factory=list
    )

    intent_indexes: list[int] = field(
        default_factory=list
    )

    metadata: dict = field(
        default_factory=dict
    )

@dataclass
class ClarificationResponse:

    answers: dict[int, dict] = field(
        default_factory=dict
    )

@dataclass
class ExecutionPlan:

    steps: list[PlanStep] = field(
        default_factory=list
    )

@dataclass
class PendingTask:

    request_package: RequestPackage

    plan: ExecutionPlan

    clarification: ClarificationRequest

    context: RequestContext

@dataclass
class PlannerResult:

    status: str

    plan: ExecutionPlan | None = None

    clarification: ClarificationRequest | None = None

    pending_task: PendingTask | None = None

    metadata: dict = field(
        default_factory=dict
    )

@dataclass
class ReceptionResult:

    mode: str

    response: str | None = None

    requires_confirmation: bool = False

    reason: str | None = None

    context: RequestContext | None = None