from core.agents.base import SpecializedAgent


class AgentRegistry:

    def __init__(self):

        self._agents = {}


    def register(
        self,
        agent: SpecializedAgent
    ):

        name = agent.metadata.name

        self._agents[name] = agent


    def get(
        self,
        name: str
    ):

        return self._agents.get(
            name
        )


    def list_agents(
        self
    ):

        return list(
            self._agents.values()
        )


    def find_by_task(
        self,
        task: str
    ):

        return [
            agent
            for agent in self._agents.values()
            if task in agent.metadata.supported_tasks
            and agent.metadata.available
        ]