from pydantic import BaseModel, ConfigDict

class UpdatedBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )