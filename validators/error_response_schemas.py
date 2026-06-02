from pydantic import BaseModel
from typing import List

class ErrorResponse(BaseModel):
    """Schema for individual error details in the error response."""
    type: str
    message: str

class BaseErrorResponse(BaseModel):
    """Base error response schema"""
    error: ErrorResponse

class FieldErrorResponse(BaseModel):
    """Schema for field-specific error details in the error response."""
    field: str
    message: str

class CustomErrorResponse(ErrorResponse):
    """Schema for custom error messages, extending the error response."""
    message: List[FieldErrorResponse]

class ValidationErrorResponse(BaseErrorResponse):
    """Schema for validation error responses, extending the base error response."""
    error: CustomErrorResponse

class RequestJSONErrorResponse(BaseErrorResponse):
    """Schema for request JSON error responses, extending the base error response."""
    pass

class RateLimitExceededResponse(BaseErrorResponse):
    """Schema for rate limit exceeded error responses, extending the base error response."""
    pass

class ResourceNotFoundResponse(BaseErrorResponse):
    """Schema for notebook not found error responses, extending the base error response."""
    pass

class ServerErrorResponse(BaseErrorResponse):
    """Schema for server error responses with status code of 500, extending the base error response."""
    pass