from dataclasses import dataclass, field


@dataclass
class PlanStep:

    capability: str

    action: str

    parameters: dict = field(
        default_factory=dict
    )

    status: str = "pending"

    result: object | None = None

    error: str | None = None


@dataclass
class ExecutionPlan:

    steps: list[PlanStep] = field(
        default_factory=list
    )

@dataclass
class ReceptionResult:

    mode: str

    response: str | None = None

    requires_confirmation: bool = False

    reason: str | None = None

    context: dict | None = None