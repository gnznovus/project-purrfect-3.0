import pytest

from core.intent.extractor import IntentExtractor
from core.intent.models import IntentSet
from core.intent.policy import IntentExtractionPolicy
from core.llm.models import LLMResponse


class FakeLLMProvider:

    def __init__(
        self,
        content
    ):
        self.content = content


    async def complete(
        self,
        request
    ):

        return LLMResponse(
            content=self.content,
            model="fake"
        )


@pytest.mark.asyncio
async def test_intent_extractor_parse_valid_json():

    provider = FakeLLMProvider(
        """
        {
            "intents": [
                {
                    "type": "create_event",
                    "confidence": 0.95,
                    "entities": {
                        "date": "tomorrow"
                    }
                }
            ]
        }
        """
    )


    extractor = IntentExtractor(
        provider,
        IntentExtractionPolicy()
    )


    result = await extractor.extract(
        "Create an event tomorrow"
    )


    assert isinstance(
        result,
        IntentSet
    )


    assert len(
        result.intents
    ) == 1


    assert result.intents[0].type == "create_event"


@pytest.mark.asyncio
async def test_intent_extractor_invalid_json():

    provider = FakeLLMProvider(
        "not json"
    )


    extractor = IntentExtractor(
        provider,
        IntentExtractionPolicy(
            max_attempts=2
        )
    )


    with pytest.raises(
        ValueError
    ):
        await extractor.extract(
            "hello"
        )

@pytest.mark.asyncio
async def test_intent_extractor_missing_intents():

    provider = FakeLLMProvider(
        """
        {
            "message": "hello"
        }
        """
    )


    extractor = IntentExtractor(
        provider,
        IntentExtractionPolicy(
            max_attempts=1
        )
    )


    with pytest.raises(
        ValueError
    ):
        await extractor.extract(
            "hello"
        )

@pytest.mark.asyncio
async def test_intent_extractor_missing_type():

    provider = FakeLLMProvider(
        """
        {
            "intents": [
                {
                    "confidence": 0.9,
                    "entities": {}
                }
            ]
        }
        """
    )


    extractor = IntentExtractor(
        provider,
        IntentExtractionPolicy(
            max_attempts=1
        )
    )


    with pytest.raises(
        ValueError
    ):
        await extractor.extract(
            "hello"
        )