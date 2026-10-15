from core.orchestration.models import (
    ExecutionPlan
)

from core.agents.models import (
    AgentRequest
)

from core.execution.policy import (
    ExecutionPolicy
)

from core.execution.models import (
    ExecutionReport
)


class ExecutionEngine:

    def __init__(
        self,
        registry,
        policy=None
    ):
        self.registry = registry

        self.policy = (
            policy
            or ExecutionPolicy()
        )


    async def execute(
        self,
        plan: ExecutionPlan
    ) -> ExecutionReport:

        executed_steps = {}


        for step in plan.steps:

            failed_dependency = (
                self._get_failed_dependency(
                    step,
                    executed_steps
                )
            )


            if failed_dependency:

                step.status = "skipped"

                step.reason = (
                    f"dependency failed: {failed_dependency}"
                )

                executed_steps[
                    step.action
                ] = step

                continue


            await self._execute_step(
                step
            )


            executed_steps[
                step.action
            ] = step


        return ExecutionReport(
            steps=plan.steps,
            success=all(
                step.status == "completed"
                for step in plan.steps
            )
        )


    def _get_failed_dependency(
        self,
        step,
        executed_steps
    ):

        for dependency in step.depends_on:

            dependency_step = (
                executed_steps.get(
                    dependency
                )
            )

            if (
                dependency_step
                and dependency_step.status != "completed"
            ):
                return dependency


        return None


    async def _execute_step(
        self,
        step
    ):

        step.status = "running"


        agents = self.registry.find_by_task(
            step.action
        )


        if not agents:

            step.status = "failed"

            step.error = (
                "no agent found"
            )

            return


        agent = agents[0]


        for attempt in range(
            1,
            self.policy.max_attempts + 1
        ):

            try:

                result = await agent.process(
                    AgentRequest(
                        task=step.action,
                        context=step.parameters
                    )
                )


                step.status = "completed"

                step.result = result

                return


            except Exception as error:

                if attempt == self.policy.max_attempts:

                    step.status = "failed"

                    step.error = str(error)