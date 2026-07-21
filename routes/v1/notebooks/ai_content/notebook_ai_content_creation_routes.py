from uuid import UUID
from flask import g, jsonify

from validators.ai_content.creation_schemas import (
    GenerateSummaryRequest,
    GenerateQuizRequest,
    GenerateFlashcardsRequest,
    GenerateMindMapRequest,
    GenerateExamRequest
)
from app.extensions import limiter
from decorators.json_required import json_required
from decorators.login_required import login_required
from utils.ai_content_creator import start_ai_generation
from configs import get_settings
from models.enums import AIContentTypes
from services.ai_generation.generation_context import GenerationContext

from routes.v1.notebooks import notebook_bp

# Get the settings object
settings = get_settings()

# Generate a new summary route
@notebook_bp.post("<uuid:notebook_id>/summaries")
@limiter.limit(settings.AI_CONTENT_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def generate_summary_endpoint(notebook_id: UUID):
    """
    Endpoint to generate a summary based on selected uploads from a notebook.
    Expects a JSON payload with the upload ids
    """
    payload = GenerateSummaryRequest(**g.json_data)
    
    generation_context = GenerationContext(
        note_ids=payload.upload_ids
    )

    return jsonify(
        start_ai_generation(
            notebook_id=str(notebook_id), 
            user_id=g.user_id, 
            generation_context=generation_context,
            content_type=AIContentTypes.SUMMARY,
            generation_options={},
            success_message="Summary generation started"
        )
    ), 202

# Generate a new quiz route
@notebook_bp.post("<uuid:notebook_id>/quizzes")
@limiter.limit(settings.AI_CONTENT_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def generate_quiz_endpoint(notebook_id: UUID):
    """
    Endpoint to generate a quiz based on selected uploads from a notebook.
    Expects a JSON payload with the upload ids
    """
    payload = GenerateQuizRequest(**g.json_data)

    generation_context = GenerationContext(
        note_ids=payload.upload_ids
    )

    return jsonify(
        start_ai_generation(
            notebook_id=str(notebook_id), 
            user_id=g.user_id, 
            generation_context=generation_context,
            content_type=AIContentTypes.QUIZ,
            generation_options={
                "difficulty": payload.difficulty,
                "question_count": payload.question_count,
                "marks": payload.marks,
                "negative_marking": payload.negative_marking,
                "fake_provider": {
                    "questions": payload.question_count
                }
            },
            success_message="Quiz generation started"
        )
    ), 202

# Generate new flashcards route
@notebook_bp.post("<uuid:notebook_id>/flashcards")
@limiter.limit(settings.AI_CONTENT_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def generate_flashcards_endpoint(notebook_id: UUID):
    """
    Endpoint to generate flashcards based on selected uploads from a notebook.
    Expects a JSON payload with the upload ids
    """
    payload = GenerateFlashcardsRequest(**g.json_data)

    generation_context = GenerationContext(
        note_ids=payload.upload_ids
    )

    return jsonify(
        start_ai_generation(
            notebook_id=str(notebook_id), 
            user_id=g.user_id, 
            generation_context=generation_context,
            content_type=AIContentTypes.FLASHCARDS,
            generation_options={
                "total_cards": payload.total_cards,
                "fake_provider": {
                    "flashcards": payload.total_cards
                }
            },
            success_message="Flashcard generation started"
        )
    ), 202

# Generate a new mind map route
@notebook_bp.post("<uuid:notebook_id>/mind-maps")
@limiter.limit(settings.AI_CONTENT_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def generate_mind_map_endpoint(notebook_id: UUID):
    """
    Endpoint to generate a mind map based on selected uploads from a notebook.
    Expects a JSON payload with the upload ids
    """
    payload = GenerateMindMapRequest(**g.json_data)

    generation_context = GenerationContext(
        note_ids=payload.upload_ids
    )

    return jsonify(
        start_ai_generation(
            notebook_id=str(notebook_id), 
            user_id=g.user_id, 
            generation_context=generation_context,
            content_type=AIContentTypes.MIND_MAPS,
            generation_options={},
            success_message="Mind map generation started"
        )
    ), 202

# default blueprints if no blueprint provided
DEFAULT_BLUEPRINTS = {
    "quiz": "standard-quiz",
    "school": "standard-school-examination",
    "university": "standard-university-examination",
    "competitive": "standard-competitive-examination",
    "certification": "standard-certification-examination",
}

# Generate a new exam route
@notebook_bp.post("<uuid:notebook_id>/exams")
@limiter.limit(settings.AI_CONTENT_RATE_LIMIT, override_defaults=False)
@json_required
@login_required
def generate_exam_endpoint(notebook_id: UUID):
    """
    Endpoint to generate a exam based on selected uploads, reference papers, blueprint and difficulty from a notebook.
    Expects a JSON payload with the upload ids
    """
    payload = GenerateExamRequest(**g.json_data)

    if payload.blueprint_slug is None:
        payload.blueprint_slug = DEFAULT_BLUEPRINTS[payload.exam_type]
    
    generation_context = GenerationContext(
        note_ids=payload.upload_ids,
        reference_ids=payload.reference_ids,
        blueprint_slug=payload.blueprint_slug
    )

    return jsonify(
        start_ai_generation(
            notebook_id=str(notebook_id), 
            user_id=g.user_id, 
            generation_context=generation_context,
            content_type=AIContentTypes.EXAM,
            generation_options={
                "difficulty": payload.difficulty
            },
            success_message="Exam generation started"
        )
    ), 202