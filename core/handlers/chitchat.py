from core.result import CoreResult


class ChitchatHandler:

    def __init__(
        self,
        llm_service
    ):
        self.llm_service = llm_service


    async def handle(
        self,
        context
    ):

        response = await self.llm_service.complete(
            context.user_input
        )


        return CoreResult(
            type="response",
            content=response.content,
            metadata={
                "model": response.model
            }
        )