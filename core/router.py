from .handler import Handler
from core.conversation.mode import ConversationMode


class Router:

    def __init__(self):
        self._handlers: dict[str, Handler] = {}


    def register(
        self,
        mode: str,
        handler: Handler
    ):
        self._handlers[mode] = handler


    def resolve(
        self,
        mode: ConversationMode
    ) -> Handler:

        if mode not in self._handlers:
            raise ValueError(
                f"No handler registered for mode: {mode}"
            )

        return self._handlers[mode]