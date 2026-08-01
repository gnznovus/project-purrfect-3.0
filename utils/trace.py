from pathlib import Path
from datetime import datetime


TRACE_FILE = (
    Path("tests")
    / "log"
    / "test_trace.txt"
)


def write_section(
    title
):

    with TRACE_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n"
            "================================\n"
            f"{title}\n"
            f"TIME: {datetime.now()}\n"
            "================================\n\n"
        )


def write_trace(
    title,
    data
):

    with TRACE_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"[{title}]\n"
        )

        for key, value in data.items():

            file.write(
                f"{key}: {value}\n"
            )

        file.write("\n")