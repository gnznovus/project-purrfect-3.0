from core.orchestration.models import (
    ExecutionPlan
)

from core.agents.models import (
    AgentRequest
)


class ExecutionEngine:

    def __init__(
        self,
        registry
    ):
        self.registry = registry


    async def execute(
        self,
        plan: ExecutionPlan
    ) -> ExecutionPlan:


        for step in plan.steps:

            step.status = "running"


            agents = self.registry.find_by_task(
                step.action
            )


            if not agents:

                step.status = "failed"

                step.error = (
                    "no agent found"
                )

                continue


            agent = agents[0]


            try:

                result = await agent.process(
                    AgentRequest(
                        task=step.action,
                        context=step.parameters
                    )
                )


                step.status = "completed"

                step.result = result


            except Exception as error:

                step.status = "failed"

                step.error = str(error)


        return plan