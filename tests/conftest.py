from pathlib import Path
from datetime import datetime


LOG_DIR = Path(__file__).parent / "log"

VERBOSE_LOG_FILE = LOG_DIR / "test_verbose.txt"
TRACE_LOG_FILE = LOG_DIR / "test_trace.txt"
ERROR_LOG_FILE = LOG_DIR / "err.txt"


TEST_RUN_TIME = None


def pytest_configure(config):

    global TEST_RUN_TIME

    LOG_DIR.mkdir(
        exist_ok=True
    )

    TEST_RUN_TIME = datetime.now()

    VERBOSE_LOG_FILE.write_text(
        "================================\n"
        "PURRFECT TEST RUN\n"
        "================================\n"
        f"STARTED: {TEST_RUN_TIME}\n\n",
        encoding="utf-8"
    )

    TRACE_LOG_FILE.write_text(
        "================================\n"
        "PURRFECT TEST TRACE\n"
        "================================\n"
        f"STARTED: {TEST_RUN_TIME}\n\n",
        encoding="utf-8"
    )

    ERROR_LOG_FILE.write_text(
        "================================\n"
        "TEST ERROR LOG\n"
        "================================\n"
        f"STARTED: {TEST_RUN_TIME}\n\n",
        encoding="utf-8"
    )


def pytest_runtest_logreport(report):

    if report.when not in (
        "setup",
        "call",
        "teardown"
    ):
        return


    status = (
        "PASSED"
        if report.passed
        else "FAILED"
    )


    with VERBOSE_LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n"
            "------------------------------\n"
            f"TEST: {report.nodeid}\n"
            f"PHASE: {report.when}\n"
            f"STATUS: {status}\n"
            f"DURATION: {report.duration:.3f}s\n"
            "------------------------------\n"
        )


    if report.failed:

        with ERROR_LOG_FILE.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n"
                "------------------------------\n"
                f"TEST: {report.nodeid}\n"
                f"PHASE: {report.when}\n"
                "STATUS: FAILED\n"
                f"DURATION: {report.duration:.3f}s\n"
                "------------------------------\n"
                "\n"
            )

            if report.longrepr:
                file.write(
                    str(report.longrepr)
                )

                file.write(
                    "\n\n"
                )


def pytest_collectreport(report):

    if not report.failed:
        return


    with ERROR_LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n"
            "================================\n"
            "COLLECTION ERROR\n"
            "================================\n\n"
        )

        file.write(
            str(report.longrepr)
        )

        file.write(
            "\n\n"
        )