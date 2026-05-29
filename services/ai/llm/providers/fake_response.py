from exceptions import LLMError

def create_fake_response(task="summary", n=5):
    """Create a fake response for testing purposes."""
    match task:
        # Fake response for summarization task
        case "summary":
            return {
                "summary": "fake response",
                "key_points": ["1", "2", "3"],
                "important_terms": ["..."]
            }
        
        # Fake response for quiz generation task
        case "quiz":
            return {
                "questions": [
                    {
                        "question": "fake response",
                        "options": ["A", "B", "C", "D"],
                        "answer": "..."
                    } for _ in range(n)
                ]
            }
        
        # Default case for unsupported tasks
        case _:
            raise LLMError(f"unsupported task: {task}")