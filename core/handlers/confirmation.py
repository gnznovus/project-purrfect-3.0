from ..result import CoreResult
from ..state_update import StateUpdate, StateUpdateType


class ConfirmationHandler:

    async def handle(
        self,
        context
    ):

        user_input = (
            context.user_input
            .lower()
            .strip()
        )


        if user_input in (
            "yes",
            "y",
            "confirm"
        ):
            return CoreResult(
                type="state_update",
                content="confirmed",
                state_updates=[
                    StateUpdate(
                        type=StateUpdateType.CONFIRM_PENDING_ACTION
                    )
                ]
            )


        if user_input in (
            "no",
            "n",
            "reject"
        ):
            return CoreResult(
                type="state_update",
                content="rejected",
                state_updates=[
                    StateUpdate(
                        type=StateUpdateType.REJECT_PENDING_ACTION
                    )
                ]
            )


        return CoreResult(
            type="response",
            content="Please confirm or reject."
        )