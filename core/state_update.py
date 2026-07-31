from dataclasses import dataclass
from enum import Enum


class StateUpdateType(str, Enum):

    REQUEST_MODE_CHANGE = "request_mode_change"

    CONFIRM_PENDING_ACTION = "confirm_pending_action"

    REJECT_PENDING_ACTION = "reject_pending_action"

    SET_MODE = "set_mode"

    SET_ACTIVE_TASK = "set_active_task"

    CLEAR_ACTIVE_TASK = "clear_active_task"


@dataclass
class StateUpdate:

    type: StateUpdateType

    value: str | None = None

    reason: str | None = None