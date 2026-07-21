def create_flashcard_prompt(resources: str, total_cards: int) -> str:
    """Creates a prompt for generating flashcards based on the given notes and number of cards."""
    return f"""
        You are an educational flashcard designer.

        Resources:
        {resources}

        Generate exactly {total_cards} flashcards.

        Requirements:
        1. Each flashcard must test one important concept.
        2. The front should contain a concise question, keyword, or cue.
        3. The back should contain a short, accurate answer.
        4. Keep every flashcard easy to memorize.
        5. Avoid duplicate concepts.
        6. Prefer definitions, formulas, facts, and key ideas.

        STRICT RULES:
        - Return only content represented by the provided JSON schema.
        - Do not implement facts on your own.
        - Use the provided notes as base knowledge source.
    """