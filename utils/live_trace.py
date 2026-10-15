from datetime import datetime
from pathlib import Path


TRACE_FILE = Path("app") / "log" / "live_trace.txt"


def write_live_trace(title, data):
    TRACE_FILE.parent.mkdir(exist_ok=True)

    with TRACE_FILE.open("a", encoding="utf-8") as file:
        file.write(
            f"\n[{datetime.now().isoformat()}] {title}\n"
        )

        for key, value in data.items():
            file.write(f"{key}: {value}\n")
