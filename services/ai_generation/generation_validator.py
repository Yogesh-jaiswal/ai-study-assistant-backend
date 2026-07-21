from repositories.upload_repository import get_uploads_in_group
from repositories.blueprint_repository import get_blueprint_by_blueprint_slug
from exceptions import ResourceNotFoundError, ConflictError, BadRequestError
from models.enums import UploadPurpose, ProcessingStatus
from .generation_context import GenerationContext

class GenerationValidator:
    """
    Validates every resource referenced by an AI generation request.

    Validation includes:

    - existence
    - ownership / visibility
    - processing status (for uploads)
    - expected upload purpose
    - blueprint accessibility
    """
    
    @staticmethod
    def validate(resources: GenerationContext, notebook_id: str, user_id: str) -> None:
        GenerationValidator._validate_upload_resources(notebook_id, resources.note_ids, UploadPurpose.NOTES)
        
        if resources.reference_ids:
            GenerationValidator._validate_upload_resources(notebook_id, resources.reference_ids, UploadPurpose.REFERENCE)

        if resources.blueprint_slug:
            GenerationValidator._validate_blueprint(resources.blueprint_slug, user_id)

    @staticmethod
    def _validate_upload_resources(notebook_id: str, resource_ids: list[str], purpose: UploadPurpose) -> None:
        resources = get_uploads_in_group(resource_ids, notebook_id)
        
        if len(resources) != len(resource_ids):
            raise ResourceNotFoundError("One or more resources not found")
        
        for resource in resources:
            if resource.processing_status != ProcessingStatus.COMPLETED:
                raise ConflictError(
                    "All resources are not processed yet. Please wait!"
                )
            elif resource.upload_purpose != purpose:
                raise BadRequestError(
                    f"All resources must be a {purpose.value}"
                )
            
    @staticmethod
    def _validate_blueprint(slug: str, user_id: str) -> None:
        bluerprint = get_blueprint_by_blueprint_slug(slug, user_id)

        if bluerprint is None or (not bluerprint.is_public and bluerprint.created_by != user_id and not bluerprint.is_system):
            raise ResourceNotFoundError("Blueprint not found!")