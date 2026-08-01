from deepeval.models.base_model import DeepEvalBaseLLM
from google import genai

from pydantic import BaseModel

from configs import get_settings

settings = get_settings()

class DeepEvalJudge(DeepEvalBaseLLM):
    def __init__(self):
        self.client = None

    def load_model(self):
        if self.client is None:
            self.client = genai.Client(api_key=settings.MODEL_API_KEY)

        return self.client

    def get_model_name(self):
        return settings.MODEL_NAME

    def generate(self, prompt: str) -> str:
        client = self.load_model()
        
        response = client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text

    def generate_with_schema(
        self,
        prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:
        client = self.load_model()
                
        response = client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )

        if response.parsed is None:
            raise RuntimeError("Gemini failed to return structured output.")

        return response.parsed

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    async def a_generate_with_schema(
        self,
        prompt: str,
        schema: type[BaseModel],
    ) -> BaseModel:
        return self.generate_with_schema(prompt, schema)