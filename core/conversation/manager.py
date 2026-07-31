from ..state_update import StateUpdateType
from .mode import ConversationMode
from .state import ConversationState
from .pending_transition import PendingTransition


class ConversationStateManager:

    def __init__(
        self,
        state: ConversationState | None = None
    ):
        self.state = state or ConversationState()


    def get_state(
        self
    ) -> ConversationState:
        return self.state


    async def apply(
        self,
        updates
    ):
        for update in updates:

            if update.type == StateUpdateType.SET_MODE:
                self.switch_mode(
                    ConversationMode(update.value)
                )

            elif update.type == StateUpdateType.REQUEST_MODE_CHANGE:

                self.request_transition(
                    ConversationMode(update.value),
                    update.reason or ""
                )


            elif update.type == StateUpdateType.SET_ACTIVE_TASK:
                self.set_active_task(
                    update.value
                )


            elif update.type == StateUpdateType.CLEAR_ACTIVE_TASK:
                self.set_active_task(
                    None
                )


    def switch_mode(
        self,
        mode: ConversationMode
    ):
        self.state.mode = mode


    def set_active_task(
        self,
        task_id: str | None
    ):
        self.state.active_task_id = task_id

    def can_transition(
        self,
        target_mode: ConversationMode
    ) -> bool:

        current = self.state.mode

        if current == target_mode:
            return True


        allowed = {
            ConversationMode.CHITCHAT: {
                ConversationMode.PLANNER
            },
            ConversationMode.PLANNER: {
                ConversationMode.CHITCHAT,
                ConversationMode.PLANNER
            }
        }


        return (
            target_mode
            in allowed.get(current, set())
        )

    def request_transition(
        self,
        target_mode: ConversationMode,
        reason: str
    ):
        self.state.pending_transition = PendingTransition(
            from_mode=self.state.mode,
            target_mode=target_mode,
            reason=reason
        )


    def confirm_transition(
        self
    ):
        pending = self.state.pending_transition

        if pending is None:
            return


        self.switch_mode(
            pending.target_mode
        )

        self.state.pending_transition = None


    def reject_transition(
        self
    ):
        self.state.pending_transition = None

    def confirm_pending_transition(self):

        if self.state.pending_transition is None:
            return

        self.confirm_transition()


    def reject_pending_transition(self):

        self.reject_transition()