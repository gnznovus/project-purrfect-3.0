from dataclasses import dataclass, field


@dataclass
class ExecutionReport:

    steps: list = field(
        default_factory=list
    )

    success: bool = True