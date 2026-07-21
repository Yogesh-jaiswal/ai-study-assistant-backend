# Custom LLM error class
class LLMError(Exception):
    pass

# Custom response validation Error
class AIResponseValidationError(Exception):
    pass

# Custom bad request error
class BadRequestError(Exception):
    pass

# Custom resource not found error
class ResourceNotFoundError(Exception):
    pass

# Custom database error
class DatabaseError(Exception):
    pass

# Custom authentication error
class AuthenticationError(Exception):
    pass

# Custom conflict error
class ConflictError(Exception):
    pass

# custom unsupported file type error
class UnsupportedFileTypeError(Exception):
    pass