from core.agents.base import SpecializedAgent

from core.agents.models import (
    AgentMetadata
)


class ReminderAgent(
    SpecializedAgent
):

    metadata = AgentMetadata(
        name="reminder",
        version="1.0",
        domain="reminder",
        description="Reminder management specialist",

        supported_tasks=[
            "create_reminder",
            "update_reminder",
            "delete_reminder"
        ],

        input_requirements=[
            "message",
            "time"
        ],

        output_contract=[
            "result"
        ]
    )