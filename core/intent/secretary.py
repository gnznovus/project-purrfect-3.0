from core.context import RequestContext

from core.intent.models import (
    Intent,
    IntentSet,
    RequestPackage
)


class IntentSecretary:

    def __init__(
        self,
        extractor,
        capability_snapshot
    ):
        self.extractor = extractor

        self.available_tasks = {
            task
            for capability in capability_snapshot
            for task in capability["supported_tasks"]
        }


    async def process(
        self,
        context: RequestContext
    ) -> RequestPackage:

        extracted = await self.extractor.extract(
            context
        )


        normalized = self.normalize(
            extracted
        )


        return RequestPackage(
            intent_set=normalized,
            context=context
        )


    def normalize(
        self,
        intent_set: IntentSet
    ) -> IntentSet:

        intents = []


        for intent in intent_set.intents:

            if intent.type not in self.available_tasks:

                intents.append(
                    Intent(
                        type="unknown",
                        entities=intent.entities,
                        confidence=intent.confidence,
                        context=(
                            intent.context
                            or intent.type
                        )
                    )
                )

                continue


            intents.append(
                intent
            )


        return IntentSet(
            intents=intents
        )