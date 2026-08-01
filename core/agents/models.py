from dataclasses import dataclass, field


@dataclass
class AgentMetadata:

    name: str

    version: str

    domain: str

    description: str


    supported_tasks: list[str] = field(
        default_factory=list
    )


    input_requirements: list[str] = field(
        default_factory=list
    )


    output_contract: list[str] = field(
        default_factory=list
    )


    related_tools: list[str] = field(
        default_factory=list
    )


    collaboration: bool = False


    available: bool = True


@dataclass
class AgentRequest:

    task: str

    context: dict = field(
        default_factory=dict
    )


@dataclass
class AgentResult:

    domain: str

    result: str | None = None

    confidence: float | None = None

    missing_information: list[str] = field(
        default_factory=list
    )

    recommendations: list[str] = field(
        default_factory=list
    )

    risks: list[str] = field(
        default_factory=list
    )