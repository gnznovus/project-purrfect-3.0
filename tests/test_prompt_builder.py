from core.intent.prompt_builder import (
    IntentPromptBuilder
)


def test_prompt_builder():

    snapshot = [
        {
            "name": "weather",
            "description": "Weather specialist",
            "supported_tasks": [
                "get_weather"
            ],
            "input_requirements": [
                "location"
            ]
        }
    ]


    prompt = IntentPromptBuilder().build(
        snapshot
    )


    assert (
        "weather"
        in prompt
    )


    assert (
        "get_weather"
        in prompt
    )


    assert (
        "location"
        in prompt
    )