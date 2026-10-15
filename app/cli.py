import asyncio

from core.conversation.mode import ConversationMode
from core.orchestration.reception import ReceptionAgent
from core.orchestration.response import ResponseBuilder

from app.bootstrap import build_application


async def run():
    components = build_application()
    application = components.application
    conversation = components.conversation
    reception = ReceptionAgent()
    response_builder = ResponseBuilder()

    print("Purrfect 3.0 demo. Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            break

        if not user_input:
            continue

        if conversation.get_state().mode == ConversationMode.CHITCHAT:
            reception_result = await reception.process(user_input)

            if reception_result.mode == "planner":
                conversation.request_transition(
                    ConversationMode.PLANNER,
                    reception_result.reason or "task detected",
                    original_message=user_input
                )

                print("Purrfect: " + response_builder.build_mode_confirmation(
                    reception_result.reason or "task detected"
                ))

                continue

        result = await application.handle_message(user_input)
        print(f"Purrfect: {result.content or result.type}")

        if result.type == "error":
            print(f"Details: {result.metadata.get('error', 'unknown error')}")


if __name__ == "__main__":
    asyncio.run(run())
