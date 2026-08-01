import httpx


class OllamaClient:

    def __init__(
        self,
        base_url="http://localhost:11434"
    ):
        self.base_url = base_url


    async def chat(
        self,
        model,
        messages
    ):

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                }
            )

            response.raise_for_status()

            return response.json()