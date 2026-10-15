from core.orchestration.models import (
    PendingTask
)


class WorkingMemory:

    def __init__(
        self
    ):
        self._pending_task: PendingTask | None = None


    def store(
        self,
        task: PendingTask
    ):
        self._pending_task = task


    def get_pending(
        self
    ) -> PendingTask | None:
        return self._pending_task


    def has_pending(
        self
    ) -> bool:
        return self._pending_task is not None


    def clear(
        self
    ):
        self._pending_task = None