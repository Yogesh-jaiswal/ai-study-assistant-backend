def create_mind_maps_prompt(resources: str) -> str:
    """Creates a prompt for generating a mid map of the given notes."""
    return f"""
        You are an educational mind map designer.

        Resources:
        {resources}

        Generate a hierarchical mind map representing the most important concepts.

        Requirements:

        1. Create a single root node representing the overall topic.
        2. Organize related concepts into logical branches.
        3. Each child should represent a refinement of its parent.
        4. Keep node text concise (prefer keywords or short phrases).
        5. Avoid duplicate concepts.
        6. Use multiple levels when appropriate.
        7. Include only concepts supported by the notes.

        STRICT RULES:
        - Return only content represented by the provided JSON schema.
        - Do not implement facts on your own.
        - Use the provided notes as base knowledge source.
    """