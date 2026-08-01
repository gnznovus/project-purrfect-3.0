from core.intent.models import (
    Intent,
    IntentSet,
    RequestPackage
)


class IntentSecretary:

    def __init__(
        self,
        extractor
    ):
        self.extractor = extractor


    async def process(
        self,
        user_input
    ):

        result = await self.extractor.extract(
            user_input
        )


        if isinstance(
            result,
            IntentSet
        ):
            intent_set = result

        else:
            intent_set = IntentSet(
                intents=[
                    result
                ]
            )


        return RequestPackage(
            intent_set=intent_set
        )