from typing import Any

from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory

class FakeProvider:

    def generate(self, prompt: str, response_schema: type[BaseModel]) -> dict[str, Any]:
        class Factory(ModelFactory):
            __model__ = response_schema


        return Factory.build().model_dump()