from dataclasses import dataclass, field
from typing import Any


@dataclass
class CoreResult:
    type: str

    content: str | None = None

    state_updates: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)