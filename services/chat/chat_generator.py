from configs import get_settings
from services.ai.engine import AIEngine

from .chat_prompt import create_ask_prompt
from .chat_schema import ChatResponse


class ChatGenerator:

    def __init__(self):

        self.engine = AIEngine(get_settings().AI_MODEL)

    def generate(self, question: str, context: str):

        prompt = create_ask_prompt(question, context)

        return self.engine.complete(prompt, ChatResponse)