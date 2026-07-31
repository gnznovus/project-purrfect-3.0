from pathlib import Path
from datetime import datetime


LOG_DIR = Path(__file__).parent / "log"

VERBOSE_LOG_FILE = LOG_DIR / "test_verbose.txt"
ERROR_LOG_FILE = LOG_DIR / "err.txt"


def pytest_configure(config):

    LOG_DIR.mkdir(
        exist_ok=True
    )

    now = datetime.now()

    VERBOSE_LOG_FILE.write_text(
        f"TEST RUN STARTED: {now}\n\n",
        encoding="utf-8"
    )

    ERROR_LOG_FILE.write_text(
        f"TEST ERROR LOG STARTED: {now}\n\n",
        encoding="utf-8"
    )


def pytest_runtest_logreport(report):

    if report.when != "call":
        return


    status = "PASSED" if report.passed else "FAILED"


    with VERBOSE_LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n"
            f"TEST: {report.nodeid}\n"
            f"STATUS: {status}\n"
            "\n"
        )


    if report.failed:

        with ERROR_LOG_FILE.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n"
                f"TEST: {report.nodeid}\n"
                f"STATUS: FAILED\n"
                "\n"
            )

            if report.longrepr:
                file.write(
                    str(report.longrepr)
                )

                file.write(
                    "\n\n"
                )