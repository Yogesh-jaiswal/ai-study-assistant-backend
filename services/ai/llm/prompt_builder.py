def create_summary_prompt(topic, notes):
    """Creates a prompt for generating a summary of the given topic and notes."""
    return f"""
        You are a study-focused tutor.

        Topic: {topic}
        Notes: {notes}

        Do the following:
        1. Summarize the notes
        2. Give at least 3 key points
        3. Give important terms

        Summary should answer:
        - what is this topic about?
        - what are the core ideas?
        - what should be remembered later?

        STRICT RULES:
        - Return ONLY valid JSON
        - No explanations
        - No text outside JSON

        Format:
        {{
            "summary": "...",
            "key_points": ["...", "..."],
            "important_terms": ["...", "..."]
        }}
    """

def create_quiz_prompt(topic, notes, n, level):
    """Creates a prompt for generating quiz questions based on the given topic, notes, number of questions, and difficulty level."""
    return f"""
        You are a quiz designer

        Topic: {topic}
        Notes: {notes}

        Do the following:
            1. Questions would be {level} difficult
            2. Create {n} quiz questions
            3. Create 4 options
            4. Add the answer

        STRICT RULES:
        - Return ONLY valid JSON
        - No explanations
        - No text outside JSON

        Format:
        {{
            "questions": [
                {{
                    "question": "...",
                    "options": ["A", "B", "C", "D"],
                    "answer": "..."
                }}
            ]
        }}
    """