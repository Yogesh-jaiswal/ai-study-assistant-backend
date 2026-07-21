import shutil
from pathlib import Path

from pytest import fixture
from configs import get_settings

@fixture(scope="session", autouse=True)
def cleanup_uploads():
    yield

    upload_dir = Path(get_settings().UPLOAD_FOLDER)

    if upload_dir.exists():
        shutil.rmtree(upload_dir)