from core.orchestration.models import (
    ExecutionPlan,
    PlanStep
)


class PlannerAgent:

    async def create_plan(
        self,
        request_package
    ) -> ExecutionPlan:

        plan = ExecutionPlan()


        for intent in request_package.intent_set.intents:

            plan.steps.append(
                PlanStep(
                    capability="calendar",
                    action=intent.type,
                    parameters=intent.entities
                )
            )


        return plan


    async def process(
        self,
        request_package
    ) -> ExecutionPlan:

        return await self.create_plan(
            request_package
        )