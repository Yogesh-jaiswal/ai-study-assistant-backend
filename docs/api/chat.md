# Chat API

The Chat API allows users to ask natural language questions about the contents of a notebook.

Unlike other AI features, chat responses are generated synchronously and returned immediately within the HTTP request.

The response is grounded using the notebook's uploaded resources through the Retrieval pipeline described in [retrieval.md](../architecture/retrieval.md).

Every chat request belongs to exactly one notebook.

---

# Authorization

Protected endpoints require the following header:

```http
Authorization: Bearer <access_token>
```

Missing, expired, or invalid access tokens result in:

```
401 Unauthorized
```

---

# Chat Flow

Every chat request follows the retrieval pipeline before reaching the language model.

```
Question
      ↓
Similarity Search
      ↓
Context Assembly
      ↓
Prompt Construction
      ↓
AI Response
      ↓
Response + Citations
```

The backend only answers using information retrieved from the notebook.

If the requested information cannot be found, the assistant returns an appropriate fallback response rather than generating unsupported information.

---

# Endpoint

## Ask Question

**POST**

```
/v1/notebooks/{notebook_id}/ask
```

Generates a grounded AI response using the notebook's uploaded resources.

Unlike summaries, quizzes, flashcards, and exams, this endpoint executes synchronously and immediately returns the generated answer.

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| question | string | Yes | User question |

### Validation

- Minimum length: 10 characters
- Maximum length: 500 characters
- Leading and trailing whitespace is removed
- Cannot be empty after trimming

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "response": "Paris is the capital city of France.",
        "citations": [
            {
                "filename": "geography.pdf",
                "source_type": "pdf",
                "author": "John Doe",
                "metadata": {
                    "page": 9
                }
            }
        ]
    },
    "error": null
}
```

### Citation Metadata

Citation metadata depends on the uploaded resource type.

Examples include:

| Source | Metadata |
|--------|----------|
| PDF | `page` |
| CSV | `row_range` |
| Markdown | *(currently none)* |
| DOCX | *(currently none)* |
| TXT | *(currently none)* |
| Image | *(currently none)* |
| YouTube | `start`, `end` |

Additional metadata may be introduced for supported document types in future releases.

### Fallback Response

If no relevant notebook content is found, the endpoint still returns **200 OK** with the following response:

```json
{
    "success": true,
    "data": {
        "response": "Sorry, I couldn't find the information in your notes.",
        "citations": []
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 404 | Notebook not found |
| 422 | Validation error |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

# Architecture

The Chat API follows the same modular AI feature architecture used throughout the backend.

The implementation consists of:

- Response schema
- Prompt builder
- Generator

Unlike other AI features, chat does not execute through the asynchronous AI generation job pipeline.

Instead, it owns its own service module responsible for:

- retrieval
- context assembly
- prompt construction
- response generation
- citation generation

This keeps the synchronous request lifecycle isolated from the asynchronous AI generation architecture while still reusing the shared AI engine.

---

# Current Limitations

The current implementation intentionally keeps chat stateless.

Each request is processed independently.

Conversation history is not currently stored or reused between requests.

---

# Future Improvements

Potential future enhancements include:

- Conversation history
- Multi-turn memory
- Streaming responses
- Conversation management
- Retrieval reranking
- Query rewriting
- Hybrid retrieval
- Citation highlighting

These improvements extend the chat layer without changing the overall retrieval architecture.

---

# Common Error Responses

| Status | Description |
|--------|-------------|
| 400 | Request does not contain a valid JSON body |
| 401 | Authentication failed |
| 404 | Requested notebook does not exist or is not owned by the authenticated user |
| 422 | Request validation failed |
| 429 | Too many requests |
| 500 | Unexpected server error or database error |