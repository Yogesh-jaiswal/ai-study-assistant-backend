from typing import Literal

def create_quiz_prompt(resources: str, question_count: int, difficulty: Literal["easy", "medium", "hard"]) -> str:
    """Creates a prompt for generating quiz questions based on the given notes, number of questions, and difficulty level."""
    return f"""
        You are an educational quiz designer.

        Resources:
        {resources}

        Generate exactly {question_count} multiple-choice questions.

        Requirements:
        1. Difficulty: {difficulty}
        2. Each question must test a different concept.
        3. Each question must contain exactly four answer options.
        4. Exactly one option must be correct.
        5. The answer field must contain only the label of the correct option (A, B, C or D).
        6. Provide a concise explanation for why the correct answer is correct.

        STRICT RULES:
        - Return only content represented by the provided JSON schema.
        - Do not include any additional text.
        - Do not implement facts on your own.
        - Use the provided notes as base knowledge source.
    """