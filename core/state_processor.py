class StateUpdateProcessor:

    def __init__(self, state_manager):
        self.state_manager = state_manager


    async def process(self, updates):

        await self.state_manager.apply(
            updates
        )