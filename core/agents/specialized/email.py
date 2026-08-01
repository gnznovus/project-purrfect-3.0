from core.agents.base import SpecializedAgent

from core.agents.models import (
    AgentMetadata
)


class EmailAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="email",
        version="1.0",
        domain="email",
        description="Email communication specialist",

        supported_tasks=[
            "send_email",
            "draft_email",
            "search_email"
        ],

        input_requirements=[
            "recipient",
            "content"
        ],

        output_contract=[
            "result"
        ]
    )