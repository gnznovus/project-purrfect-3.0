from .context import RequestContext
from .result import CoreResult
from .router import Router
from utils.live_trace import write_live_trace


class CoreEngine:

    def __init__(
        self,
        router: Router,
        state_processor=None,
        confirmation_handler=None
    ):
        self.router = router
        self.state_processor = state_processor
        self.confirmation_handler = confirmation_handler


    async def process(
        self,
        context: RequestContext
    ) -> CoreResult:

        try:

            if (
                context.conversation_state.pending_transition
                and self.confirmation_handler
            ):
                result = await self.confirmation_handler.handle(
                    context
                )

            else:
                handler = self.router.resolve(
                    context.conversation_state.mode
                )

                result = await handler.handle(
                    context
                )

                if result is None:
                    raise RuntimeError(
                        "Handler returned invalid result"
                    )

            if (
                self.state_processor
                and result.state_updates
            ):
                await self.state_processor.process(
                    result.state_updates
                )


            return result

        except Exception as error:
            write_live_trace(
                "CORE ERROR",
                {
                    "request_id": context.request_id,
                    "error": str(error),
                    "user_input": context.user_input
                }
            )

            return CoreResult(
                type="error",
                content="An internal error occurred.",
                metadata={
                    "error": str(error)
                }
            )
