from core.orchestration.models import (
    ExecutionPlan
)

from core.agents.models import (
    AgentRequest,
    AgentResult
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
    ) -> list[AgentResult]:

        results = []


        for step in plan.steps:

            agents = self.registry.find_by_task(
                step.action
            )


            if not agents:
                continue


            agent = agents[0]


            result = await agent.process(
                AgentRequest(
                    task=step.action,
                    context=step.parameters
                )
            )


            results.append(
                result
            )


        return results