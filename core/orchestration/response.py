from core.orchestration.models import (
    ExecutionPlan
)


class ResponseBuilder:

    def build(
        self,
        plan: ExecutionPlan
    ) -> dict:

        results = []

        for step in plan.steps:

            if step.status == "completed":

                results.append(
                    {
                        "action": step.action,
                        "status": "completed",
                        "result": step.result.result
                    }
                )

            else:

                results.append(
                    {
                        "action": step.action,
                        "status": "failed",
                        "error": step.error
                    }
                )


        return {
            "success": all(
                step["status"] == "completed"
                for step in results
            ),
            "results": results
        }