import json

from core.context import RequestContext

from core.llm.models import (
    LLMRequest
)

from core.llm.provider import (
    LLMProvider
)

from core.intent.models import (
    IntentSet,
    Intent
)

from core.intent.policy import (
    IntentExtractionPolicy
)

from core.intent.prompts import (
    INTENT_SYSTEM_PROMPT
)

from core.intent.prompt_builder import (
    IntentPromptBuilder
)

from utils.trace import (
    write_trace
)
from utils.live_trace import write_live_trace


class IntentExtractor:

    def __init__(
        self,
        provider: LLMProvider,
        policy: IntentExtractionPolicy,
        prompt_builder: IntentPromptBuilder | None = None
    ):

        self.provider = provider

        self.policy = policy

        self.prompt_builder = (
            prompt_builder
            or IntentPromptBuilder()
        )


    async def extract(
        self,
        context: RequestContext
    ) -> IntentSet:

        system_prompt = (
            self.build_system_prompt(
                context
            )
        )


        last_response = None


        for _ in range(
            self.policy.max_attempts
        ):

            response = await self.provider.complete(
                LLMRequest(
                    system_prompt=system_prompt,
                    prompt=context.user_input,
                    metadata={"response_format": "json"}
                )
            )


            last_response = response.content

            write_live_trace(
                "INTENT LLM RESPONSE",
                {
                    "request_id": context.request_id,
                    "content": response.content
                }
            )


            try:

                return self.parse(
                    response.content
                )


            except (
                ValueError,
                KeyError,
                json.JSONDecodeError
            ):

                continue


        write_trace(
            "LLM RAW RESPONSE",
            {
                "content": last_response
            }
        )


        raise ValueError(
            "Unable to extract valid intent"
        )


    def build_system_prompt(
        self,
        context: RequestContext
    ) -> str:

        capabilities = (
            context.metadata.get(
                "capabilities",
                []
            )
        )


        if not capabilities:

            return INTENT_SYSTEM_PROMPT


        capability_prompt = (
            self.prompt_builder.build(
                capabilities
            )
        )


        return (
            INTENT_SYSTEM_PROMPT
            + "\n\n"
            + capability_prompt
        )


    def parse(
        self,
        content: str
    ) -> IntentSet:

        content = self.clean_json(
            content
        )


        data = json.loads(
            content
        )


        if "intents" not in data:

            raise ValueError(
                "Missing intents field"
            )


        intents = [
            Intent(
                type=item["type"],
                entities=item.get(
                    "entities",
                    {}
                ),
                confidence=item.get(
                    "confidence",
                    0.0
                ),
                context=item.get(
                    "context"
                )
            )
            for item in data["intents"]
        ]


        return IntentSet(
            intents=intents
        )


    def clean_json(
        self,
        content: str
    ) -> str:

        content = content.strip()


        if content.startswith(
            "```"
        ):

            lines = content.splitlines()


            lines = [
                line
                for line in lines
                if not line.strip().startswith(
                    "```"
                )
            ]


            content = "\n".join(
                lines
            )


        return content.strip()
