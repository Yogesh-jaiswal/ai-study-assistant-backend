# Legacy AI API

The Legacy AI API contains the original text-based AI generation endpoints that existed before the Notebook-based AI architecture.

These endpoints are **deprecated** and remain available only for backward compatibility.

New applications should use the Notebook AI Content API instead.

---

# Deprecation Notice

The endpoints documented here have been superseded by the Notebook AI Content API.

Unlike the current architecture, these endpoints:

- Do not require notebooks.
- Accept raw text directly.
- Execute generation synchronously.
- Do not create AI Content resources.
- Do not support retrieval or uploaded study material.

They are retained only to preserve compatibility with older clients.

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

# Endpoints

## Generate Summary

**POST**

```
/v1/summarize
```

Generates a study summary directly from the supplied text.

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| topic | string | Yes | Topic title |
| notes | string | Yes | Raw study notes |

### Validation

#### topic

- Minimum length: 1 character
- Maximum length: 100 characters
- Leading and trailing whitespace is removed
- Cannot be empty after trimming

#### notes

- Minimum length: 10 characters
- Maximum length: Configured backend limit
- Leading and trailing whitespace is removed
- Cannot be empty after trimming

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "summary": "...",
        "key_points": [
            "...",
            "...",
            "..."
        ],
        "important_terms": [
            "...",
            "..."
        ]
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Generate Quiz

**POST**

```
/v1/quiz
```

Generates quiz questions directly from the supplied text.

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| topic | string | Yes | Topic title |
| notes | string | Yes | Raw study notes |
| n | integer | No | Number of quiz questions |
| level | string | No | Difficulty level (`easy`, `medium`, `hard`) |

### Validation

#### topic

- Minimum length: 1 character
- Maximum length: 100 characters
- Leading and trailing whitespace is removed
- Cannot be empty after trimming

#### notes

- Minimum length: 10 characters
- Maximum length: Configured backend limit
- Leading and trailing whitespace is removed
- Cannot be empty after trimming

#### n

- Minimum value: 1
- Maximum value: Configured backend limit

#### level

Allowed values:

- easy
- medium
- hard

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "questions": [
            {
                "question": "...",
                "options": [
                    "...",
                    "...",
                    "...",
                    "..."
                ],
                "answer": "..."
            }
        ]
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

# Common Error Responses

| Status | Description |
|--------|-------------|
| 400 | Request does not contain a valid JSON body |
| 401 | Authentication failed |
| 422 | Request validation failed |
| 429 | Too many requests |
| 500 | Unexpected server error |