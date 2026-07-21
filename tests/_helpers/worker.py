import os
import subprocess
import time
from typing import IO
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

print(os.getenv("ENVIRONMENT"))

# Configuration
WORKER_TIMEOUT = 60

# Log file
LOG_DIR = Path("tests/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class WorkerProcess:
    process: subprocess.Popen
    log_handle: IO[str] | None
    log_file: Path


def start_worker() -> WorkerProcess:
    """
    Starts a Celery worker.

    Returns
    -------
    WorkerProcess[
        process: subprocess.Popen,
        log_handle: IO[str] | None,
        log_file: Path
    ]
        Worker process and log file handle.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"celery_{timestamp}.log"

    debug_worker = os.getenv("DEBUG_WORKER") == "1"

    if debug_worker:
        log_handle = None

        process = subprocess.Popen(
            [
                "celery",
                "-A",
                "app.worker",
                "worker",
                "--pool=solo",
                "--loglevel=info",
            ]
        )

    else:
        log_handle = open(log_file, "w", encoding="utf-8")

        process = subprocess.Popen(
            [
                "celery",
                "-A",
                "app.worker",
                "worker",
                "--pool=solo",
                "--loglevel=warning",
            ],
            stdout=log_handle,
            stderr=subprocess.STDOUT,
        )

    return WorkerProcess(
        process=process,
        log_handle=log_handle,
        log_file=log_file
    )


def wait_until_ready(worker: WorkerProcess, timeout: int = WORKER_TIMEOUT):
    """
    Wait until the Celery worker starts accepting tasks.
    """

    start = time.time()

    while time.time() - start < timeout:

        result = subprocess.run(
            [
                "celery",
                "-A",
                "app.worker",
                "inspect",
                "ping",
            ],
            capture_output=True,
            text=True,
        )

        if (
            result.returncode == 0
            and "pong" in result.stdout.lower()
        ):
            return

        time.sleep(1)

    raise RuntimeError(
        f"Celery worker failed to start within {timeout} seconds.\n"
        f"Check worker logs at: {worker.log_file}"
    )


def stop_worker(worker: WorkerProcess):
    """
    Gracefully shuts down the worker.
    """

    if worker.process.poll() is None:
        worker.process.terminate()

        try:
            worker.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            worker.process.kill()
            worker.process.wait()

    if worker.log_handle is not None:
        worker.log_handle.close()