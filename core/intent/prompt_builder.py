class IntentPromptBuilder:

    def build(
        self,
        snapshot: list[dict]
    ) -> str:

        if not snapshot:

            return (
                "AVAILABLE CAPABILITIES:\n"
                "No capabilities available."
            )


        lines = [
            "AVAILABLE CAPABILITIES:"
        ]


        for capability in snapshot:

            lines.append(
                ""
            )

            lines.append(
                f"Capability: {capability['name']}"
            )


            if capability.get(
                "description"
            ):
                lines.append(
                    f"Description: "
                    f"{capability['description']}"
                )


            tasks = capability.get(
                "supported_tasks",
                []
            )


            lines.append(
                "Supported tasks:"
            )


            for task in tasks:

                lines.append(
                    f"- {task}"
                )


            requirements = capability.get(
                "input_requirements",
                []
            )


            if requirements:

                lines.append(
                    "Input requirements:"
                )


                for requirement in requirements:

                    lines.append(
                        f"- {requirement}"
                    )


        return "\n".join(
            lines
        )