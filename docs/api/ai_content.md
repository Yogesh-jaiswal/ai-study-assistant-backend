# AI Content API

The AI Content API manages AI-generated study resources for notebook uploads.

Supported AI content includes:

- Summaries
- Quizzes
- Flashcards
- Mind Maps
- Exams

AI generation is performed asynchronously.

Every generated resource belongs to exactly one notebook owned by an authenticated user.

All AI Content endpoints require authentication.

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

# Pagination

Listing endpoints support pagination using query parameters.

| Parameter | Default | Description |
|-----------|---------|-------------|
| page | 1 | Page number |
| limit | 20 | Number of records returned |

The server enforces a maximum limit configured by the backend.

---

# AI Generation

AI content is generated asynchronously after a generation request is accepted.

Generation requests immediately return a background task identifier.

The requested content becomes available only after the generation task completes successfully.

Generated content may be retrieved through the AI Content endpoints once generation finishes.

---

# Background Task Polling

Generating AI content starts a background task.

Successful generation requests return a `task_id` that should be used to monitor generation progress.

Task status is retrieved using the Infrastructure API:

`GET /v1/tasks/{task_id}`

The task status endpoint reports:

- Current execution status
- Task type
- Generated resource identifier after successful completion
- Error information if generation fails

See the [Infrastructure API](infrastructure.md#get-task-status) documentation for the complete polling workflow and response format.

---

# AI Content Types

The backend currently supports the following AI-generated resources.

| Type | Description |
|------|-------------|
| Summary | Concise study notes generated from uploaded resources |
| Quiz | Multiple-choice questions with explanations |
| Flashcards | Question-answer flashcards for revision |
| Mind Map | Hierarchical concept map generated from uploaded content |
| Exam | Complete examination generated using notebook content and an optional blueprint |

Each content type has its own request schema and response format.

---

# AI Generation Context

Generation requests operate on uploaded notebook resources.

Depending on the requested AI content, additional generation resources may also be supplied.

| Resource | Used By |
|----------|---------|
| Notes uploads | All AI content |
| Reference uploads | Exams |
| Blueprint | Exams |

If an exam request does not provide a blueprint, the backend automatically selects an appropriate internal system blueprint based on the requested exam type.

---

# Endpoints
## Generate Summary

**POST**

```
/v1/notebooks/{notebook_id}/summaries
```

Generates an AI summary from one or more uploaded notebook resources.

Generation starts asynchronously.

The returned `task_id` should be used to monitor generation progress.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| upload_ids | string[] | Yes | Upload identifiers used to generate the summary |

### Validation

- At least one upload must be provided.
- Upload identifiers must be unique.
- Every upload identifier must be a valid UUID.

### Success Response

**202 Accepted**

```json
{
    "success": true,
    "data": {
        "task_id": "a87d9eb9-0bd1-4e66-91b3-f67d61e4ef31",
        "message": "Summary generation started"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 404 | Notebook or uploads not found |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## Generate Quiz

**POST**

```
/v1/notebooks/{notebook_id}/quizzes
```

Generates a multiple-choice quiz from one or more uploaded notebook resources.

Generation starts asynchronously.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| upload_ids | string[] | Yes | Upload identifiers used for generation |
| question_count | integer | No | Number of questions to generate |
| difficulty | string | No | Difficulty (`easy`, `medium`, `hard`) |
| marks | integer | No | Marks awarded per question |
| negative_marking | integer | No | Negative marks deducted for incorrect answers |

### Default Values

| Field | Default |
|------|---------|
| question_count | 5 |
| difficulty | medium |
| marks | 1 |
| negative_marking | 0 |

### Validation

- Upload identifiers must be unique.
- Every upload identifier must be a valid UUID.
- Marks must be greater than or equal to 1.
- Negative marking must be greater than or equal to 0.
- Difficulty must be one of:

```
easy
medium
hard
```

### Success Response

**202 Accepted**

```json
{
    "success": true,
    "data": {
        "task_id": "86c97bb4-df97-4327-9629-1fb4d80a4018",
        "message": "Quiz generation started"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 404 | Notebook or uploads not found |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## Generate Flashcards

**POST**

```
/v1/notebooks/{notebook_id}/flashcards
```

Generates revision flashcards from one or more uploaded notebook resources.

Generation starts asynchronously.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| upload_ids | string[] | Yes | Upload identifiers used for generation |
| total_cards | integer | Yes | Number of flashcards to generate |

### Validation

- Upload identifiers must be unique.
- Every upload identifier must be a valid UUID.

### Success Response

**202 Accepted**

```json
{
    "success": true,
    "data": {
        "task_id": "2a739dd7-d5c7-48b7-a7b4-8d7b3afcb842",
        "message": "Flashcard generation started"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 404 | Notebook or uploads not found |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## Generate Mind Map

**POST**

```
/v1/notebooks/{notebook_id}/mind-maps
```

Generates a hierarchical mind map from one or more uploaded notebook resources.

Generation starts asynchronously.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| upload_ids | string[] | Yes | Upload identifiers used for generation |

### Validation

- Upload identifiers must be unique.
- Every upload identifier must be a valid UUID.

### Success Response

**202 Accepted**

```json
{
    "success": true,
    "data": {
        "task_id": "2e792ca9-8b83-4a62-b4cc-fdb1cf4de08a",
        "message": "Mind map generation started"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 404 | Notebook or uploads not found |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## Generate Exam

**POST**

```
/v1/notebooks/{notebook_id}/exams
```

Generates an examination from uploaded notebook resources.

Generation may optionally use:

- reference uploads
- a blueprint
- difficulty configuration

If no blueprint is provided, the backend automatically selects an appropriate internal system blueprint based on the requested exam type.

Generation starts asynchronously.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| upload_ids | string[] | Yes | Upload identifiers used for generation |
| reference_ids | string[] | No | Reference uploads used during generation |
| blueprint_slug | string | No | Blueprint identifier |
| difficulty | string | Yes | Difficulty (`easy`, `medium`, `hard`, `mixed`) |
| exam_type | string | Yes | Default blueprint category when no blueprint is supplied |

### Supported Exam Types

```
quiz
school
university
competitive
certification
```

### Supported Difficulty Levels

```
easy
medium
hard
mixed
```

### Validation

- Upload identifiers must be unique.
- Reference identifiers, when provided, must be unique.
- Every identifier must be a valid UUID.

### Success Response

**202 Accepted**

```json
{
    "success": true,
    "data": {
        "task_id": "d874df6f-7fa8-44d5-bcb7-733a66157f3d",
        "message": "Exam generation started"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 404 | Notebook, uploads or blueprint not found |
| 422 | Request validation failed |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## List AI Contents

**GET**

```
/v1/notebooks/{notebook_id}/ai-contents
```

Returns all AI-generated resources belonging to the specified notebook.

The endpoint returns metadata only. The complete AI-generated content can be retrieved using the **Get AI Content** endpoint.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Query Parameters

Pagination is supported using the standard `page` and `limit` parameters.

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "ai_contents": [
            {
                "id": "ef81d9b0-cb53-4c1c-bef9-c3c237fd26e4",
                "title": "Operating System Summary",
                "type": "summary",
                "upload_count": 3,
                "generated_at": "2026-07-22T14:31:18Z"
            },
            {
                "id": "cbef7eb0-cb0d-4385-9ec7-f5d846d4bbdf",
                "title": "Computer Networks Quiz",
                "type": "quiz",
                "upload_count": 2,
                "generated_at": "2026-07-21T18:04:55Z"
            }
        ]
    },
    "error": null
}
```

### Response Fields

| Field | Description |
|------|-------------|
| id | AI content UUID |
| title | AI-generated title |
| type | Type of AI content |
| upload_count | Number of uploads used during generation |
| generated_at | Generation timestamp |

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid access token |
| 404 | Notebook not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Get AI Content

**GET**

```
/v1/notebooks/{notebook_id}/ai-contents/{ai_content_id}
```

Returns the complete AI-generated resource.

The response includes both metadata and the generated content.

The structure of the `content` field depends on the AI content type.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |
| ai_content_id | AI Content UUID |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "id": "ef81d9b0-cb53-4c1c-bef9-c3c237fd26e4",
        "title": "Operating System Summary",
        "type": "summary",
        "upload_count": 3,
        "generated_at": "2026-07-22T14:31:18Z",
        "content": {
            "...": "..."
        }
    },
    "error": null
}
```

### Response Fields

| Field | Description |
|------|-------------|
| id | AI content UUID |
| title | AI-generated title |
| type | AI content type |
| upload_count | Number of uploads used during generation |
| generated_at | Generation timestamp |
| content | Complete AI-generated content |

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid access token |
| 404 | Notebook or AI content not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Delete AI Content

**DELETE**

```
/v1/notebooks/{notebook_id}/ai-contents/{ai_content_id}
```

Deletes an AI-generated resource owned by the authenticated user.

Deleting AI content does not modify notebook uploads or background tasks.

Only the generated resource itself is removed.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |
| ai_content_id | AI Content UUID |

### Success Response

**204 No Content**

The endpoint returns an empty response body.

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid access token |
| 404 | Notebook or AI content not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

# AI Content Schemas

Every AI-generated resource consists of two parts:

1. Common metadata shared by every AI content type.
2. A type-specific `content` object.

---

## Common Metadata

Every AI-generated resource includes the following metadata.

| Field | Type | Description |
|------|------|-------------|
| id | string | Unique identifier of the generated AI content |
| title | string | AI-generated title |
| type | string | AI content type |
| upload_count | integer | Number of uploads used during generation |
| generated_at | datetime | Timestamp when generation completed |

---

## Summary

Summary content contains a concise overview of the uploaded material.

### JSON example

```json
{
  "title": "Introduction to Operating Systems",
  "summary": "...",
  "key_points": [
    "...",
    "..."
  ],
  "important_terms": [
    "...",
    "..."
  ]
}
```

---

## Quiz

Quiz content represents a multiple-choice examination.

### JSON example

```json
{
  "title": "...",
  "marks_per_question": 2,
  "negative_marking": 1,
  "difficulty": "medium",
  "questions": [
    {
      "question_id": "334b5c20-f73b-4ac6-aa80-ef74d67c00cf",
      "question": "...",
      "options": [
        {
            "label": "A",
            "text": "..."
        },
        {
            "label": "B",
            "text": "..."
        },
        {
            "label": "C",
            "text": "..."
        },
        {
            "label": "D",
            "text": "..."
        }
      ],
      "answer": "B",
      "explanation": "..."
    }
  ]
}
```

---

## Flashcards

Flashcards are generated for quick revision.

### JSON example

```json
{
    "title": "Use of Operating Systems",
    "total_cards": 1,
    "flashcards": [
        {
            "front": "...",
            "back": "..."
        }
    ]
}
```

---

## Mind Maps

Mind maps organize concepts into a hierarchical tree.

### JSON example

```json
{
    "title": "How AI agents work",
    "root": {
        "label": "...",
        "children": [
            {
                "label": "...",
                "children": [
                    {
                        "label": "...",
                        "children": []
                    }
                ]
            },
            {
                "label": "...",
                "children": []
            }
        ]
    }
}
```

The structure is recursive until leaf nodes are reached.

---

## Exams

Exam content represents the final examination produced by merging the selected blueprint with AI-generated question content.

The blueprint defines the examination structure, while the AI generates the examination title, shared materials, questions, and answer options.

### JSON example

```json
{
  "title": "Mock Test",
  "difficulty": "mixed",
  "exam_name": "JEE Main Paper 1",
  "description": "...",
  "duration": "3 hours",
  "total_marks": 100,
  "navigation_rules": {
    "allow_cross_section_navigation": true,
    "has_sectional_timers": false,
    "is_computer_adaptive": false
  },
  "sections": [
    {
      "section_name": "Physics",
      "total_marks": 100,
      "section_duration": null,
      "question_groups": [
        {
          "group_title": "Multiple Choice Questions",
          "selection_rule": {
            "type": "all"
          },
          "defaults": {
            "question_type": "MCQ",
            "answer_type": "single_choice",
            "negative_marking": 1
          },
          "parts": [
            {
              "label": "Q1-Q20",
              "count": 20,
              "marks": 4
            }
          ],
          "shared_material": null,
          "questions": [
            {
              "question_id": "68437d69-4c07-4ba9-b439-14e21d2c5f7b",
              "question_label": "Q1",
              "question": "...",
              "marks": 4,
              "negative_marking": 1,
              "options": [
                {
                  "label": "A",
                  "text": "..."
                },
                {
                  "label": "B",
                  "text": "..."
                },
                {
                  "label": "C",
                  "text": "..."
                },
                {
                  "label": "D",
                  "text": "..."
                }
              ]
            }
          ],
          "alternatives": null
        },
        {
          "group_title": "Attempt Any One",
          "selection_rule": {
            "type": "or"
          },
          "defaults": {
            "question_type": "Numerical",
            "answer_type": "numeric",
            "negative_marking": 1
          },
          "parts": null,
          "shared_material": null,
          "questions": null,
          "alternatives": [
            {
              "title": "Alternative A",
              "parts": [
                {
                  "label": "Q21-Q25",
                  "count": 5,
                  "marks": 4
                }
              ],
              "questions": [
                {
                  "question_id": "ce28913f-9884-4a23-a1aa-d91bf2b72c85",
                  "question_label": "Q21",
                  "question": "...",
                  "marks": 4,
                  "negative_marking": 1,
                  "options": null
                },
                {
                  "question_id": "55f09409-c022-48ba-9c1f-b78eb5141a5d",
                  "question_label": "Q22",
                  "question": "...",
                  "marks": 4,
                  "negative_marking": 1,
                  "options": null
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

The final examination is created by merging two independent sources.

**The blueprint provides:**

- examination metadata
- navigation rules
- section layout
- question groups
- question distribution
- attempt rules
- answer types
- marking scheme
- internal choice structure

**The AI provides:**

- examination title
- shared materials
- question statements
- answer options

**During post-processing the backend additionally injects:**

- unique `question_id` for every generated question
- marks from the corresponding blueprint part
- negative marking from the blueprint defaults
- selected generation difficulty

---

# AI Content Post-processing

Before AI content is stored, the backend performs additional processing depending on the generated resource.

### Summary

- Normalizes the generated title.

### Quiz

- Normalizes the generated title.
- Adds a unique `question_id` to every generated question.
- Injects:
  - difficulty
  - marks per question
  - negative marking

### Flashcards

- Normalizes the generated title.
- Injects `total_cards`.

### Mind Maps

- Normalizes the generated title.

### Exams

- Normalizes the generated title.
- Merges AI-generated content into the selected blueprint.
- Preserves all blueprint-defined examination structure.
- Injects:
  - unique `question_id`
  - marks
  - negative marking
  - selected generation difficulty

---

# Common Error Responses

| Status | Description |
|--------|-------------|
| 400 | Request does not contain a valid JSON body |
| 401 | Authentication failed |
| 404 | Requested notebook, AI content, upload, or blueprint does not exist |
| 422 | Request validation failed |
| 429 | Too many requests |
| 500 | Unexpected server error or Database errors |