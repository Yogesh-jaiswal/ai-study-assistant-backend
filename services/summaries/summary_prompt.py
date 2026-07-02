def create_summary_prompt(topic: str, notes: str) -> str:
    """Creates a prompt for generating a summary of the given topic and notes."""
    return f"""
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
        - No explanations
    """