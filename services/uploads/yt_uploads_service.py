import logging

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from models import Upload
from models.enums import ProcessingStatus, FileTypes
from repositories.notebook_repository import get_notebook_by_notebook_id
from repositories.upload_repository import save_upload
from tasks.processing_task import process_file
from services.integrations.redis_service import set_key
from validators.upload_schemas import YoutubeUploadRequest

from exceptions import ResourceNotFoundError, BadRequestError

# Set up logging
logger = logging.getLogger(__name__)

# YoutubeDL object configuration options
YDL_OPTIONS = {
    "quiet": True,
    "skip_download": True,
}

def upload_yt_video(notebook_id: str, user_id: str, payload: YoutubeUploadRequest) -> dict[str, str]:
    """Creates a new upload for a notebook."""
    video_url = payload.url

    notebook = get_notebook_by_notebook_id(notebook_id, user_id)
    if not notebook:
        raise ResourceNotFoundError(f"notebook with id {notebook_id} not found")
    
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(video_url, download=False)
    except DownloadError:
        logger.exception("Failed to fetch YouTube metadata")
        raise BadRequestError("Unable to retrieve YouTube video")
        
    filename = info.get("title") or "YouTube Video"

    source_type = FileTypes.YOUTUBE

    upload = Upload(
        notebook_id=notebook_id, 
        filename=filename, 
        source_type=source_type, 
        processing_status=ProcessingStatus.PENDING, 
        file_path=video_url
    )

    save_upload(upload)

    task = process_file.delay(notebook_id, user_id, upload.id)

    set_key(
        f"task:{task.id}:owner",
        user_id,
        86400
    )

    set_key(
        f"task:{task.id}:type",
        "upload",
        86400
    )

    return {
        "upload_id": upload.id,
        "task_id": task.id
    }