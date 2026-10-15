class ConfirmationGate:

    def check(
        self,
        reception_result
    ) -> bool:

        return (
            reception_result.requires_confirmation
        )


    async def confirm(
        self,
        approved: bool
    ) -> bool:

        return approved