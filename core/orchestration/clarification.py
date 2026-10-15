import json

from core.llm.models import LLMRequest
from core.orchestration.models import ClarificationResponse


class ClarificationExtractor:

    def __init__(self, provider):
        self.provider = provider

    async def extract(self, user_input, pending_task):
        intents = pending_task.request_package.intent_set.intents
        prompt = {
            "questions": pending_task.clarification.questions,
            "intent_indexes": pending_task.clarification.intent_indexes,
            "intents": [
                {
                    "index": index,
                    "type": intent.type,
                    "entities": intent.entities,
                    "context": intent.context
                }
                for index, intent in enumerate(intents)
            ],
            "user_answer": user_input
        }

        response = await self.provider.complete(
            LLMRequest(
                system_prompt=(
                    "Extract answers to the clarification questions. "
                    "Return only valid JSON in this format: "
                    '{"answers":{"intent_index":{"type":"task_name",'
                    '"entities":{},"context":"updated objective"}}}. '
                    "Keep existing intent types when the answer only adds "
                    "missing information. Do not answer the user."
                ),
                prompt=json.dumps(prompt),
                metadata={"response_format": "json"}
            )
        )

        data = json.loads(response.content.strip())
        from utils.live_trace import write_live_trace

        write_live_trace(
            "CLARIFICATION LLM RESPONSE",
            {
                "user_input": user_input,
                "content": response.content
            }
        )
        answers = data.get("answers", {})

        if "intent_index" in answers:
            answer = answers["intent_index"]
            target_indexes = pending_task.clarification.intent_indexes

            if target_indexes:
                answers = {
                    str(target_indexes[0]): answer
                }

        for index, answer in list(answers.items()):
            if isinstance(answer, str):
                question = pending_task.clarification.questions[0].lower()
                field = next(
                    (
                        candidate
                        for candidate in (
                            "destination",
                            "date",
                            "title",
                            "recipient",
                            "content",
                            "query",
                            "time"
                        )
                        if candidate in question
                    ),
                    "details"
                )
                answers[index] = {
                    "entities": {field: answer},
                    "context": answer
                }

        if not isinstance(answers, dict):
            raise ValueError("Clarification answers must be an object.")

        return ClarificationResponse(
            answers={
                int(index): answer
                for index, answer in answers.items()
                if str(index).isdigit()
            }
        )
