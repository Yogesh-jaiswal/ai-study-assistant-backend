# Custom LLM error class
class LLMError(Exception):
    pass

# Custom response validation Error
class ResponseValidationError(Exception):
    pass

# Custom empty request JSON error
class RequestJSONError(Exception):
    pass