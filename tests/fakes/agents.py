from core.agents.specialized.weather import WeatherAgent

from core.agents.models import AgentRequest, AgentResult

class FailingWeatherAgent(
    WeatherAgent
):

    async def process(
        self,
        request: AgentRequest
    ) -> AgentResult:

        raise Exception(
            "weather service unavailable"
        )