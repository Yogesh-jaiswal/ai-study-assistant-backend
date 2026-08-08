from .attempt_bundle import EvaluationBundle
from .attempt_context import AttemptContext
from repositories.ai_content_repository import get_ai_content_by_content_id

class AttemptLoader:
    """
    Loads validated attempt resources and assembles a EvaluationBundle.

    The builder transforms lightweight identifiers stored in
    AttemptContext into fully loaded resources that AI jobs can
    directly consume.
    """
    def load(context: AttemptContext, notebook_id: str, user_id: str):
        ai_content = get_ai_content_by_content_id(notebook_id, user_id, context.content_id)

        return EvaluationBundle(
            question_paper=ai_content.content,
            submitted_answers=context.answers
        )