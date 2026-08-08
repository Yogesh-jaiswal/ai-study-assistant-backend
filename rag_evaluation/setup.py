import json
import time
from pathlib import Path

from flask import Flask

from werkzeug.datastructures import FileStorage

from app.factory import create_app

from validators.auth.register_schamas import RegistrationRequest
from validators.notebook_schemas import CreateNotebookRequest

from services.auth.register_service import register_user
from services.notebooks.notebook_service import create_notebook
from services.uploads.upload_service import upload_file
from services.task_status.task_service import task_status

from repositories.user_repository import get_user_by_id
from repositories.notebook_repository import get_notebook_by_notebook_id
from repositories.upload_repository import get_upload_by_upload_id

from models.enums import ProcessingStatus, UploadPurpose

# Constants for evaluation setup
EVALUATION_EMAIL = "Evaluate123@test.com"
EVALUATION_USERNAME = "evaluate123"
EVALUATION_PASSWORD = "Evaluate123@"
EVALUATION_NOTEBOOK = "RAG Evaluation Dataset"
STATE_FILE = "rag_evaluation/state.json"
CORPUS_FILE = "rag_evaluation/corpus.md"

def load_state() -> dict:
    """Loads the evaluation state from a JSON file if it exists, otherwise returns an empty dictionary."""
    if Path(STATE_FILE).exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}

def setup() -> tuple[Flask, dict]:
    """Sets up the Flask application and ensures that the necessary user, notebook, and upload exist for evaluation. If they do not exist, it creates them and persists the state to a JSON file."""
    app = create_app()

    state = load_state()

    user_id = state.get("user_id")
    notebook_id = state.get("notebook_id")
    upload_id = state.get("upload_id")

    with app.app_context():
        if user_id is None or get_user_by_id(user_id) is None:
            print("Creating User...")
            registration_payload = RegistrationRequest(
                email=EVALUATION_EMAIL,
                username=EVALUATION_USERNAME,
                password=EVALUATION_PASSWORD
            )

            user = register_user(registration_payload)

            user_id = user.id

            print("User created\n")

        if notebook_id is None or get_notebook_by_notebook_id(notebook_id, user_id) is None:
            print("Creating Notebook...")
            notebook_payload = CreateNotebookRequest(
                title=EVALUATION_NOTEBOOK
            )

            notebook_id = create_notebook(user_id, notebook_payload)

            print("Notebook created\n")

        if upload_id is None or get_upload_by_upload_id(notebook_id, user_id, upload_id) is None:
            print("Creating Upload...")
            with open(CORPUS_FILE, "rb") as f:
                file = FileStorage(
                    stream=f,
                    filename="corpus.md",
                    content_type="text/markdown",
                )

                response = upload_file(
                    notebook_id,
                    user_id,
                    file,
                    UploadPurpose.NOTES
                )

                task_id = response["task_id"]
                upload_id = response["upload_id"]

                print("Waiting for the upload processing...")

                while (True):
                    task_response = task_status(task_id, user_id)

                    if task_response["status"] == "SUCCESS":
                        if task_response["result"] is None or task_response["result"]["file_status"] != ProcessingStatus.COMPLETED:
                            raise RuntimeError("Upload task failed")
                        break

                    if task_response["status"] == "FAILED":
                        raise RuntimeError("Upload task failed")

                    time.sleep(1)

                print("Upload completed\n")

        state = {
            "user_id": user_id,
            "notebook_id": notebook_id,
            "upload_id": upload_id
        }

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
            print("State persisted")

        return app, state