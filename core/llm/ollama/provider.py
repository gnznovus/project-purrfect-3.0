from core.llm.models import (
    LLMRequest,
    LLMResponse
)

from core.llm.provider import LLMProvider
from core.llm.config import LLMConfig


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        client,
        config: LLMConfig,
    ):
        self.client = client
        self.config = config


    async def complete(
        self,
        request: LLMRequest
    ) -> LLMResponse:

        messages = []

        if request.system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": request.system_prompt
                }
            )


        messages.append(
            {
                "role": "user",
                "content": request.prompt
            }
        )


        response_format = None

        if request.metadata:
            response_format = request.metadata.get(
                "response_format"
            )

        request_options = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature
        }

        if response_format:
            request_options["response_format"] = response_format

        response = await self.client.chat(
            **request_options
        )


        return LLMResponse(
            content=response["message"]["content"],
            model=self.config.model
        )
