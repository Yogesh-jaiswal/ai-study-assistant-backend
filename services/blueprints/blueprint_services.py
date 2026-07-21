from typing import Any
from copy import deepcopy
from slugify import slugify
from models import ExamBlueprint
from repositories.blueprint_repository import (
    save_blueprint,
    get_blueprint_by_blueprint_slug,
    list_blueprints,
    update_blueprint,
    remove_blueprint,
    list_matching_slugs
)
from validators.blueprint_schemas import BlueprintCreationRequest
from exceptions import ResourceNotFoundError
from utils.slug_creator import generate_unique_slug

def create_blueprint(user_id: str, payload: BlueprintCreationRequest) -> str:
    """Creates a new blueprint"""
    slug = slugify(payload.structure.exam_name)

    blueprint = ExamBlueprint(
        slug=generate_unique_slug(payload.structure.exam_name, list_matching_slugs(slug)),
        name=payload.structure.exam_name,
        description=payload.structure.description,
        created_by=user_id,
        is_public=payload.is_public,
        structure=payload.structure.model_dump()
    )

    save_blueprint(blueprint)

    return blueprint.slug

def list_public_blueprints(keyword: str | None = None, limit: int = 20, offset: int = 0) -> dict[str, Any]:
    """Get public blueprints by keyword"""
    blueprints = list_blueprints(
        public_only=True,
        keyword=keyword,
        limit=limit,
        offset=offset
    )

    return [
        {
            "id": blueprint.id,
            "slug": blueprint.slug,
            "name": blueprint.name,
            "description": blueprint.description,
            "is_public": blueprint.is_public,
            "owner": blueprint.created_by,
            "created_at": blueprint.created_at.isoformat()
        } for blueprint in blueprints
    ]

def list_user_blueprints(user_id: str, keyword:str | None = None, limit: int = 20, offset: int = 0) -> dict[str, Any]:
    """Get user blueprints by keywrord"""
    blueprints = list_blueprints(
        owner_id=user_id,
        keyword=keyword,
        limit=limit,
        offset=offset
    )

    return [
        {
            "id": blueprint.id,
            "slug": blueprint.slug,
            "name": blueprint.name,
            "description": blueprint.description,
            "is_public": blueprint.is_public,
            "owner": blueprint.created_by,
            "created_at": blueprint.created_at.isoformat()
        } for blueprint in blueprints
    ]

def get_blueprint_by_slug(slug: str, user_id: str):
    """Get the blueprint using slug"""
    blueprint = get_blueprint_by_blueprint_slug(slug, user_id)

    if blueprint is None or (not blueprint.is_public and blueprint.created_by != user_id):
        raise ResourceNotFoundError("Blueprint not found!")
    
    return {
        "id": blueprint.id,
        "slug": blueprint.slug,
        "name": blueprint.name,
        "description": blueprint.description,
        "is_public": blueprint.is_public,
        "owner": blueprint.created_by,
        "structure": blueprint.structure,
        "created_at": blueprint.created_at.isoformat()
    }

def copy_blueprint(slug: str, user_id: str) -> str:
    """Copy public blueprint to user's collection"""
    old_blueprint = get_blueprint_by_blueprint_slug(slug, user_id)

    if old_blueprint is None or old_blueprint.is_system:
        raise ResourceNotFoundError("Blueprint not found!")

    if old_blueprint.created_by == user_id:
        return old_blueprint.slug
    
    new_slug = slugify(old_blueprint.name)
    
    new_blueprint = ExamBlueprint(
        slug = generate_unique_slug(old_blueprint.name, list_matching_slugs(new_slug)),
        name = old_blueprint.name,
        description = old_blueprint.description,
        created_by = user_id,
        structure = deepcopy(old_blueprint.structure)
    )

    save_blueprint(new_blueprint)

    return new_blueprint.slug

def edit_blueprint(slug: str, user_id: str, payload: BlueprintCreationRequest) -> None:
    """Edit the old blueprint with the new data"""
    blueprint = get_blueprint_by_blueprint_slug(slug, user_id)

    if blueprint is None:
        raise ResourceNotFoundError("Blueprint not found!")
    
    if blueprint.is_public and blueprint.created_by != user_id:
        new_blueprint_id = copy_blueprint(slug, user_id)
        blueprint = get_blueprint_by_blueprint_slug(slug, user_id)
    
    new_slug = slugify(payload.structure.exam_name)

    blueprint.slug = generate_unique_slug(payload.structure.exam_name, list_matching_slugs(new_slug))
    blueprint.name = payload.structure.exam_name
    blueprint.description = payload.structure.description
    blueprint.is_public = payload.is_public
    blueprint.structure = payload.structure.model_dump()

    update_blueprint(blueprint)

    return blueprint.slug

def delete_blueprint(slug: str, user_id: str) -> None:
    """Deletes a specific blueprint owned by user"""
    blueprint = get_blueprint_by_blueprint_slug(slug, user_id)

    if blueprint is None or blueprint.created_by != user_id:
        raise ResourceNotFoundError("Blueprint not found!")
    
    remove_blueprint(blueprint)