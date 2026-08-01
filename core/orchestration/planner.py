from core.orchestration.models import (
    ExecutionPlan,
    PlanStep
)


class PlannerAgent:

    def __init__(
        self,
        registry
    ):

        self.registry = registry


    async def create_plan(
        self,
        request_package
    ) -> ExecutionPlan:

        plan = ExecutionPlan()


        for intent in request_package.intent_set.intents:

            agents = self.registry.find_by_task(
                intent.type
            )


            if not agents:
                continue


            selected_agent = agents[0]


            plan.steps.append(
                PlanStep(
                    capability=(
                        selected_agent.metadata.domain
                    ),
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