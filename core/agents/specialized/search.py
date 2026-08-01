from core.agents.base import SpecializedAgent

from core.agents.models import (
    AgentMetadata
)


class SearchAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="search",
        version="1.0",
        domain="search",
        description="Information retrieval specialist",

        supported_tasks=[
            "web_search",
            "knowledge_search"
        ],

        input_requirements=[
            "query"
        ],

        output_contract=[
            "results"
        ]
    )