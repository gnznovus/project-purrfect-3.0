from core.execution.models import (
    ExecutionReport
)
import json

class ResponseBuilder:

    def __init__(self, llm_service=None):
        self.llm_service = llm_service

    async def build_clarification(
        self,
        clarification,
        user_input=None
    ) -> str:
        missing_requirements = clarification.metadata.get(
            "missing_requirements",
            []
        )

        if missing_requirements and isinstance(
            missing_requirements[0],
            list
        ):
            missing_requirements = missing_requirements[0]

        requested_field = (
            missing_requirements[0]
            if missing_requirements
            else None
        )

        if self.llm_service:
            response = await self.llm_service.complete(
                "Continue the planning task. The planner's main job is to "
                "complete the user's objective, not to start general chat. "
                "If required information is missing, ask one focused "
                "question about exactly one field listed in "
                "missing_requirements. Never ask for fields that are not "
                "listed there. If the user asks for advice or a recommendation, "
                "answer briefly or suggest an option relevant to the task. "
                "Otherwise acknowledge the answer and continue planning. "
                "Do not invent extra requirements or repeatedly say 'can you "
                "confirm'. Do not mention indexes, schemas, agents, or JSON. "
                "Return only the response text.\n\n"
                + json.dumps({
                    "missing_questions": clarification.questions,
                    "missing_requirements": missing_requirements,
                    "only_ask_about": requested_field,
                    "latest_user_input": user_input
                })
            )
            return response.content

        questions = clarification.questions

        if not questions:
            return "I need a little more information before planning that."

        return "I need a little more information:\n" + "\n".join(
            f"{index + 1}. {question}"
            for index, question in enumerate(questions)
        )

    def build_plan(self, plan) -> str:
        if not plan.steps:
            return "I could not find any actionable steps."

        steps = "\n".join(
            f"{index + 1}. {step.action}"
            for index, step in enumerate(plan.steps)
        )

        return f"Here is the plan:\n{steps}"

    def build_mode_confirmation(self, reason) -> str:
        return (
            f"I detected a task ({reason}). "
            "Would you like to enter planning mode?"
        )

    def build_confirmation_prompt(self) -> str:
        return "Should I execute this plan?"

    def build_invalid_confirmation(self) -> str:
        return "Please confirm or reject."

    def build(
        self,
        report: ExecutionReport
    ) -> dict:

        results = []

        for step in report.steps:

            result = {
                "action": step.action,
                "status": step.status
            }

            if step.status == "completed":

                result["result"] = (
                    step.result.result
                )

            elif step.status == "failed":

                result["error"] = step.error

            elif step.status == "skipped":

                result["reason"] = step.reason

            results.append(
                result
            )


        return {
            "success": report.success,
            "results": results
        }
