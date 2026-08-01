import pytest

from core.intent.secretary import IntentSecretary
from core.intent.models import RequestPackage


class FakeIntentExtractor:

    async def extract(
        self,
        user_input
    ):

        from core.intent.models import Intent

        return Intent(
            type="chitchat",
            confidence=1.0
        )


@pytest.mark.asyncio
async def test_secretary_extracts_user_intent():

    secretary = IntentSecretary(
        FakeIntentExtractor()
    )


    result = await secretary.process(
        "hello"
    )


    assert isinstance(
        result,
        RequestPackage
    )


    assert len(
        result.intent_set.intents
    ) == 1


    intent = result.intent_set.intents[0]


    assert intent.type == "chitchat"

    assert intent.confidence == 1.0