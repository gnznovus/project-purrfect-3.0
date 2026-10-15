from core.orchestration.models import (
    ExecutionPlan,
    PlanStep,
    PlannerResult,
    ClarificationRequest,
    PendingTask,
    ClarificationResponse
)

from utils.trace import write_trace
from utils.live_trace import write_live_trace


class PlannerAgent:

    def __init__(
        self,
        registry
    ):
        self.registry = registry


    async def create_plan(
        self,
        request_package
    ) -> PlannerResult:

        write_live_trace(
            "PLANNER INTENT STATE",
            {
                "stage": "before_plan",
                "intents": [
                    {
                        "index": index,
                        "type": intent.type,
                        "entities": intent.entities,
                        "context": intent.context
                    }
                    for index, intent in enumerate(
                        request_package.intent_set.intents
                    )
                ]
            }
        )

        if not request_package.intent_set.intents:

            raise ValueError(
                "No actionable intents"
            )


        plan = ExecutionPlan()

        clarifications = []


        for index, intent in enumerate(
            request_package.intent_set.intents
        ):

            #
            # Unknown intent
            #

            if intent.type == "unknown":

                clarifications.append(
                    {
                        "intent_index": index,
                        "reason": "unknown_intent",
                        "context": intent.context
                    }
                )

                continue


            #
            # Capability lookup
            #

            agents = self.registry.find_by_task(
                intent.type
            )

            write_trace(
                "PLANNER LOOKUP",
                {
                    "intent": intent.type,
                    "found": [
                        agent.metadata.name
                        for agent in agents
                    ]
                }
            )


            if not agents:

                clarifications.append(
                    {
                        "intent_index": index,
                        "reason": "missing_capability",
                        "context": intent.context
                    }
                )

                continue


            selected_agent = agents[0]

            missing_requirements = [
                requirement
                for requirement in selected_agent.metadata.input_requirements
                if not self._has_requirement(
                    intent.entities,
                    requirement
                )
            ]

            if missing_requirements:
                clarifications.extend(
                    {
                        "intent_index": index,
                        "reason": "missing_information",
                        "missing_requirements": missing_requirements,
                        "context": self._clarification_question(
                            intent.type,
                            missing_requirements
                        )
                    }
                    for _ in [0]
                )

                continue


            plan.steps.append(
                PlanStep(
                    step_type="execute",
                    capability=(
                        selected_agent.metadata.domain
                    ),
                    action=intent.type,
                    parameters=intent.entities,
                    context=intent.context
                )
            )


        #
        # Return clarification request
        #

        if clarifications:

            clarification = ClarificationRequest(
                reason="missing_information",
                questions=[
                    item["context"]
                    for item in clarifications
                ],
                intent_indexes=[
                    item["intent_index"]
                    for item in clarifications
                ],
                metadata={
                    "missing_requirements": [
                        item.get("missing_requirements", [])
                        for item in clarifications
                    ]
                }
            )

            return PlannerResult(
                status="needs_clarification",
                plan=plan,
                clarification=clarification,
                pending_task=PendingTask(
                    request_package=request_package,
                    plan=plan,
                    clarification=clarification,
                    context=request_package.context
                )
            )


        #
        # Ready for execution
        #

        return PlannerResult(
            status="ready",
            plan=plan
        )

    async def resume(
        self,
        pending_task: PendingTask,
        clarification_response: ClarificationResponse
    ) -> PlannerResult:

        request_package = pending_task.request_package

        intents = (
            request_package
            .intent_set
            .intents
        )

        for index, answer in (
            clarification_response.answers.items()
        ):

            if index >= len(intents):
                continue

            intent = intents[index]

            intent.type = answer.get(
                "type",
                intent.type
            )

            intent.entities.update(
                answer.get(
                    "entities",
                    {}
                )
            )

            intent.context = (
                answer.get("context") or intent.context
            )

        write_trace(
            "RESUME BEFORE PLAN",
            {
                "types": [
                    intent.type
                    for intent in (
                        request_package.intent_set.intents
                    )
                ]
            }
        )

        return await self.create_plan(
            request_package
        )

        write_live_trace(
            "PLANNER INTENT UPDATE",
            {
                "answers": clarification_response.answers,
                "intents": [
                    {
                        "index": index,
                        "type": intent.type,
                        "entities": intent.entities,
                        "context": intent.context
                    }
                    for index, intent in enumerate(intents)
                ]
            }
        )

    def _clarification_question(
        self,
        intent_type,
        requirements
    ):
        fields = ", ".join(requirements)

        return (
            f"To {intent_type.replace('_', ' ')}, "
            f"what {fields} should I use?"
        )

    def _has_requirement(
        self,
        entities,
        requirement
    ):
        if entities.get(requirement):
            return True

        aliases = {
            "date": {
                "date_range",
                "start_date",
                "end_date"
            }
        }

        return any(
            entities.get(alias)
            for alias in aliases.get(requirement, set())
        )

    async def process(
        self,
        request_package
    ) -> PlannerResult:

        return await self.create_plan(
            request_package
        )
