from typing import Literal


def create_exam_prompt(
    resources: str,
    difficulty: Literal["easy", "medium", "hard", "mixed"],
) -> str:
    """Creates a prompt for generating an examination paper."""

    return f"""
        You are an expert examination paper setter.

        Your task is to generate a complete examination paper from the provided resources.

        {resources}

        RESOURCE PRIORITY

        If multiple resources conflict, follow this priority:

        1. Exam Blueprint
        2. Knowledge Source (Notes)
        3. Reference Papers

        RESOURCE RULES

        Knowledge Source
        - Treat the notes as the only factual source.
        - Never introduce facts not supported by the notes.

        Reference Papers
        - Use them only to learn formatting, presentation, language, and question sequencing.
        - Never copy questions or wording.

        Exam Blueprint
        - If present, treat it as authoritative.
        - Follow every structural constraint exactly.
        - Never modify:
        - sections
        - question counts
        - marks
        - ordering
        - selection rules
        - Generate only the question content.

        If no blueprint is provided:
        - Design a balanced examination paper yourself.
        - Use a logical structure.
        - Distribute marks fairly.
        - Avoid unnecessary repetition.
        - Choose appropriate question types.

        TARGET DIFFICULTY

        Requested Difficulty: {difficulty}

        Difficulty Guide

        Easy
        - Recall
        - Definitions
        - Basic understanding

        Medium
        - Application
        - Reasoning
        - Multi-step thinking

        Hard
        - Analysis
        - Design
        - Numerical reasoning
        - Critical thinking

        Mixed
        - Combine all difficulty levels naturally.

        GENERAL REQUIREMENTS

        - Questions must be clear and unambiguous.
        - Avoid duplicate concepts.
        - Cover the important topics proportionally.
        - Ensure marks reflect question complexity.
        - Produce a realistic examination paper suitable for students.

        STRICT RULES

        - Return ONLY the JSON matching the provided response schema.
        - Do not return markdown.
        - Do not return explanations.
        - Do not wrap the JSON in code fences.
    """