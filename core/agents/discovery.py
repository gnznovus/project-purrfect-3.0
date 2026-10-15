import importlib
import inspect
import os


from core.agents.base import (
    SpecializedAgent
)


class AgentDiscovery:

    def __init__(
        self,
        package="core.agents.specialized"
    ):
        self.package = package


    def discover(
        self
    ) -> list[SpecializedAgent]:

        agents = []


        package_path = (
            self.package.replace(
                ".",
                "/"
            )
        )


        for filename in os.listdir(
            package_path
        ):

            if not filename.endswith(
                ".py"
            ):
                continue


            if filename.startswith(
                "_"
            ):
                continue


            module_name = (
                f"{self.package}."
                f"{filename[:-3]}"
            )


            module = importlib.import_module(
                module_name
            )


            for _, obj in inspect.getmembers(
                module,
                inspect.isclass
            ):

                if (
                    issubclass(
                        obj,
                        SpecializedAgent
                    )
                    and obj is not SpecializedAgent
                ):

                    agents.append(
                        obj()
                    )


        return agents