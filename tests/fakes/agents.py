from core.agents.base import SpecializedAgent

from core.agents.models import (
    AgentMetadata,
    AgentRequest,
    AgentResult
)

from utils.trace import write_trace


class FakeCalendarAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="calendar",
        version="1.0",
        domain="calendar",
        description="Calendar specialist",

        supported_tasks=[
            "create_event",
            "update_event"
        ],

        input_requirements=[
            "title",
            "date"
        ],

        output_contract=[
            "result"
        ]
    )


    async def process(
        self,
        request: AgentRequest
    ):

        write_trace(
            "CALENDAR AGENT",
            {
                "task": request.task
            }
        )

        return AgentResult(
            domain="calendar",
            result="event created",
            confidence=1.0
        )


class FakeWeatherAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="weather",
        version="1.0",
        domain="weather",
        description="Weather specialist",

        supported_tasks=[
            "get_weather"
        ],

        input_requirements=[
            "location"
        ],

        output_contract=[
            "forecast"
        ]
    )


    async def process(
        self,
        request: AgentRequest
    ):

        write_trace(
            "WEATHER AGENT",
            {
                "task": request.task
            }
        )

        return AgentResult(
            domain="weather",
            result="sunny",
            confidence=1.0
        )


class FakeTravelAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="travel",
        version="1.0",
        domain="travel",
        description="Travel specialist",

        supported_tasks=[
            "plan_trip"
        ],

        input_requirements=[
            "destination"
        ],

        output_contract=[
            "itinerary"
        ]
    )


    async def process(
        self,
        request: AgentRequest
    ):

        write_trace(
            "TRAVEL AGENT",
            {
                "task": request.task
            }
        )

        return AgentResult(
            domain="travel",
            result="trip planned",
            confidence=1.0
        )