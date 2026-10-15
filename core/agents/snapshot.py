class CapabilitySnapshotBuilder:

    def build(
        self,
        registry
    ) -> list[dict]:

        capabilities = []

        for agent in registry.list_agents():

            if not agent.metadata.available:
                continue

            capabilities.append(
                {
                    "name": agent.metadata.name,
                    "domain": agent.metadata.domain,
                    "description": (
                        agent.metadata.description
                    ),
                    "supported_tasks": (
                        agent.metadata.supported_tasks
                    )
                }
            )

        return capabilities