from core.result import CoreResult
from core.orchestration.response import ResponseBuilder


class PlannerHandler:

    def __init__(
        self,
        secretary,
        planner,
        working_memory,
        capability_snapshot=None,
        clarification_extractor=None,
        response_builder=None
    ):
        self.secretary = secretary
        self.planner = planner
        self.working_memory = working_memory
        self.capability_snapshot = capability_snapshot or []
        self.clarification_extractor = clarification_extractor
        self.response_builder = response_builder or ResponseBuilder()

    async def handle(
        self,
        context
    ):
        context.metadata["capabilities"] = self.capability_snapshot

        pending_task = self.working_memory.get_pending()

        if pending_task:
            if self.clarification_extractor is None:
                raise RuntimeError("Clarification extractor is not configured")

            planner_result = await self.planner.resume(
                pending_task,
                await self.clarification_extractor.extract(
                    context.user_input,
                    pending_task
                )
            )
        else:
            request_package = await self.secretary.process(context)
            planner_result = await self.planner.create_plan(request_package)

        if planner_result.status == "needs_clarification":
            self.working_memory.store(
                planner_result.pending_task
            )

            return CoreResult(
                type="clarification",
                content=await self.response_builder.build_clarification(
                    planner_result.clarification,
                    context.user_input
                ),
                metadata={
                    "status": planner_result.status,
                    "questions": planner_result.clarification.questions
                }
            )

        self.working_memory.clear()

        return CoreResult(
            type="plan",
            content=self.response_builder.build_plan(
                planner_result.plan
            ),
            metadata={
                "status": planner_result.status,
                "plan": planner_result.plan
            }
        )
