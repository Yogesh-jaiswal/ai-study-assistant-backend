import json
import re
import logging

from typing import Any

from .prompt_builder import (
    create_summary_prompt, 
    create_quiz_prompt
)
from .providers.fake_response import create_fake_response
from .providers.gemini_response import create_gemini_response

from exceptions import LLMError
from configs import settings

# Set up logging
logger = logging.getLogger(__name__)

def extract_json(text: str) -> dict[str, Any]:
    """Extracts the first JSON object found in the given text."""
    try:
        match = re.search(r'\{[\s\S]*\}', text, re.DOTALL)
        if not match:
            message = "no JSON object found in model response"
            logger.error(message)
            raise LLMError(message)
        
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        logger.error(f"failed to deocde model JSON: {e}")
        raise LLMError("failed to extract valid JSON from model response")

def build_prompt_for_task(payload: object, task: str) -> str:
    """Builds the appropriate prompt based on the specified task."""
    match task:
        case "summary":
            prompt = create_summary_prompt(payload.topic, payload.notes)
        case "quiz":
            prompt = create_quiz_prompt(payload.topic, payload.notes, payload.n, payload.level)
        case _:
            raise LLMError(f"unsupported task: {task}")

    return prompt

def generate_response(payload: object, task: str = "summary") -> dict[str, Any]:
    """Generates a response from the LLM based on the given payload and task."""
    task = task.lower()
    
    prompt = build_prompt_for_task(payload, task) # Build the prompt based on the task and payload

    # Send the prompt to the appropriate model based on settings and get the response
    match settings.AI_MODEL:
        case "FAKE":
            logger.info(f"sending {task} request to the fake model")

            response = create_fake_response(task, getattr(payload, "n", 5))

            logger.info("fake response received")
        case "GEMINI":
            logger.info(f"sending {task} request to the gemini")

            response = create_gemini_response(prompt)
            
            logger.info("gemini response received")
            
    # Process the response based on the model used
    if settings.AI_MODEL != "FAKE": 
        parsed = extract_json(response)
        return parsed
    else:
        return response