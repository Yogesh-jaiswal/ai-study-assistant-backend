from dataclasses import fields

from repositories.upload_repository import get_uploads_in_group
from repositories.blueprint_repository import get_blueprint_by_blueprint_slug
from .generation_bundle import GenerationBundle
from .generation_context import GenerationContext
from validators.blueprint_schemas import BlueprintSchema

class GenerationContextBuilder:
    """
    Loads validated generation resources and assembles a GenerationBundle.

    The builder transforms lightweight identifiers stored in
    GenerationContext into fully loaded resources that AI jobs can
    directly consume.
    """

    @staticmethod
    def build(notebook_id: str, resources: GenerationContext, user_id: str) -> GenerationBundle:
        notes = GenerationContextBuilder._load_upload_text(notebook_id, resources.note_ids)
        references = None
        blueprint = None

        if resources.reference_ids:
            references = GenerationContextBuilder._load_upload_text(notebook_id, resources.reference_ids)

        if resources.blueprint_slug:
            blueprint = GenerationContextBuilder._load_blueprint(resources.blueprint_slug, user_id)       

        return GenerationBundle(
            notes=notes,
            references=references,
            blueprint=blueprint
        )

    @staticmethod
    def _load_upload_text(notebook_id: str, resource_ids: list[str]) -> str:
        resources = get_uploads_in_group(resource_ids, notebook_id)

        return "\n\n".join(
            resource.raw_text for resource in resources if resource.raw_text
        )
    
    @staticmethod
    def _load_blueprint(slug: str, user_id: str) -> dict:
        blueprint = get_blueprint_by_blueprint_slug(slug, user_id)

        return BlueprintSchema(**blueprint.structure)