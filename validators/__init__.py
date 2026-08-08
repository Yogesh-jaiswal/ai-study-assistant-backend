"""
Request and response validation schemas.

Provides Pydantic schemas used to validate API inputs,
outputs, and domain-specific structures throughout the
application.
"""

from pydantic import BaseModel, ConfigDict

class UpdatedBaseModel(BaseModel):
    """Base model with extra fields forbidden."""
    model_config = ConfigDict(
        extra="forbid"
    )