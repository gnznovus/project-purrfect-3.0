import httpx

from utils.trace import write_trace


class OllamaClient:

    def __init__(
        self,
        base_url="http://localhost:11434"
    ):
        self.base_url = base_url


    async def chat(
        self,
        model,
        messages,
        temperature=0.0,
        response_format=None
    ):

        async with httpx.AsyncClient(
            timeout=120.0
        ) as client:

            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }

            if response_format:
                payload["format"] = response_format

            response = await client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )

            response.raise_for_status()

            return response.json()
