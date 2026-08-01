# Attempts API

The Attempts API manages user attempts for AI-generated study resources.

Supported attempt types include:

* Quiz attempts
* Exam attempts

Attempt evaluation is performed asynchronously.

Every attempt belongs to exactly one AI-generated resource inside a notebook owned by an authenticated user.

All Attempt endpoints require authentication.

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

| Parameter | Default | Description                |
| --------- | ------- | -------------------------- |
| page      | 1       | Page number                |
| limit     | 20      | Number of records returned |

The server enforces a maximum limit configured by the backend.

---

# Attempt Evaluation

Attempt evaluation is performed asynchronously after a submission request is accepted.

Evaluation requests immediately return a background task identifier together with the newly created attempt identifier.

The evaluated attempt becomes available only after the evaluation task completes successfully.

Applications should retrieve the evaluated attempt after the background task finishes.

---

# Background Task Polling

Submitting an attempt starts a background evaluation task.

Successful evaluation requests return a `task_id` that should be used to monitor evaluation progress.

Task status is retrieved using the Infrastructure API:

`GET /v1/tasks/{task_id}`

The task status endpoint reports:

* Current execution status
* Task type
* Evaluated attempt identifier after successful completion
* Error information if evaluation fails

See the [Infrastructure API](infrastructure.md#get-task-status) documentation for the complete polling workflow and response format.

---

# Supported Attempt Types

The backend currently supports evaluation for the following AI-generated resources.

| AI Content | Evaluation                      |
| ---------- | ------------------------------- |
| Quiz       | Automatic rule-based evaluation |
| Exam       | AI-assisted evaluation          |

Summaries, Flashcards, and Mind Maps do not currently support user attempts.

---

# Base URL

```
/v1/notebooks/{notebook_id}/contents/{content_id}/attempts
```

---

# Endpoints
## Evaluate Attempt

**POST**

```text
/v1/notebooks/{notebook_id}/contents/{content_id}/attempts
```

Creates a new user attempt for the specified AI-generated resource.

The attempt is immediately stored and queued for asynchronous evaluation.

The returned `task_id` should be used to monitor evaluation progress.

### Path Parameters

| Parameter   | Description     |
| ----------- | --------------- |
| notebook_id | Notebook UUID   |
| content_id  | AI Content UUID |

### Request Body

```json
{
  "answers": [
    {
      "question_id": "68437d69-4c07-4ba9-b439-14e21d2c5f7b",
      "answer": "B"
    }
  ]
}
```

The answer format depends on the question type.

For example:

| Question Type   | Example              |
| --------------- | -------------------- |
| Single choice   | `"B"`                |
| Multiple choice | `["A","C"]`          |
| Numerical       | `42`                 |
| Boolean         | `true`               |
| Text            | `"Operating System"` |
| Essay           | `"..."`              |

### Success Response

**202 Accepted**

```json
{
  "success": true,
  "data": {
    "task_id": "7af2f1bb-f7aa-4b58-ae58-442de0d7821b",
    "attempt_id": "1b0dca1c-8e88-42f5-ae3b-7fb857ea8df1",
    "message": "User attempt evaluation started"
  },
  "error": null
}
```

### Possible Errors

| Status | Reason                                  |
| ------ | --------------------------------------- |
| 400    | Invalid request body                    |
| 401    | Missing or invalid access token         |
| 404    | Notebook or AI content not found        |
| 422    | Request validation failed               |
| 429    | Rate limit exceeded                     |
| 500    | Internal server error or Database error |

---

## List Attempts

**GET**

```text
/v1/notebooks/{notebook_id}/contents/{content_id}/attempts
```

Returns every evaluation attempt created for the specified AI-generated resource.

Pagination is supported using the standard `page` and `limit` query parameters.

### Path Parameters

| Parameter   | Description     |
| ----------- | --------------- |
| notebook_id | Notebook UUID   |
| content_id  | AI Content UUID |

### Success Response

**200 OK**

```json
{
  "success": true,
  "data": {
    "attempts": [
      {
        "id": "1b0dca1c-8e88-42f5-ae3b-7fb857ea8df1",
        "status": "completed",
        "total_marks": 100,
        "obtained_marks": 82,
        "percentage": 82.0,
        "evaluation_type": "exam",
        "evaluated_at": "2026-07-22T18:20:11Z"
      }
    ]
  },
  "error": null
}
```

### Possible Errors

| Status | Reason                           |
| ------ | -------------------------------- |
| 401    | Missing or invalid access token  |
| 404    | Notebook or AI content not found |
| 429    | Rate limit exceeded              |
| 500    | Internal server error            |

---

## Get Attempt

**GET**

```text
/v1/notebooks/{notebook_id}/contents/{content_id}/attempts/{attempt_id}
```

Returns a fully evaluated attempt.

Only completed evaluations contain marks and evaluation content.

### Path Parameters

| Parameter   | Description     |
| ----------- | --------------- |
| notebook_id | Notebook UUID   |
| content_id  | AI Content UUID |
| attempt_id  | Attempt UUID    |

### Success Response

**200 OK**

```json
{
  "success": true,
  "data": {
    "id": "1b0dca1c-8e88-42f5-ae3b-7fb857ea8df1",
    "status": "completed",
    "total_marks": 100,
    "obtained_marks": 82,
    "percentage": 82.0,
    "evaluation_type": "exam",
    "evaluated_at": "2026-07-22T18:20:11Z",
    "evaluation": {
      "...": "..."
    }
  },
  "error": null
}
```

### Possible Errors

| Status | Reason                                     |
| ------ | ------------------------------------------ |
| 401    | Missing or invalid access token            |
| 404    | Notebook, AI content, or attempt not found |
| 429    | Rate limit exceeded                        |
| 500    | Internal server error                      |

---

# Attempt Schemas

Every evaluated attempt consists of two parts:

1. Common metadata shared by every attempt.
2. A type-specific `evaluation` object.

---

## Common Metadata

Every evaluated attempt includes the following metadata.

| Field           | Type         | Description                |
| --------------- | ------------ | -------------------------- |
| id              | string       | Attempt identifier         |
| status          | string       | Current processing status  |
| total_marks     | integer/null | Maximum obtainable marks   |
| obtained_marks  | integer/null | Marks obtained by the user |
| percentage      | number/null  | Percentage score           |
| evaluation_type | string       | Evaluation type            |
| evaluated_at    | datetime     | Evaluation timestamp       |

---

## Quiz Evaluation

Quiz evaluation contains the result for every submitted question.

### JSON Example

```json
{
  "questions": [
    {
      "question_id": "...",
      "question": "...",
      "obtained_marks": 2,
      "maximum_marks": 2,
      "status": "correct",
      "user_answer": "B",
      "correct_answer": "B",
      "explanation": "..."
    }
  ]
}
```

---

## Exam Evaluation

Exam evaluation returns the original generated examination merged with:

* submitted answers
* AI feedback
* awarded marks

### JSON Example

```json
{
  "title": "...",
  "difficulty": "mixed",
  "overall_feedback": "...",
  "sections": [
    {
      "section_name": "...",
      "obtained_marks": 28,
      "question_groups": [
        {
          "group_title": "...",
          "obtained_marks": 12,
          "questions": [
            {
              "question_id": "...",
              "question": "...",
              "marks": 4,
              "negative_marking": 1,
              "user_answer": "42",
              "obtained_marks": 4,
              "feedback": "Correct answer."
            }
          ]
        }
      ]
    }
  ]
}
```

The returned evaluation preserves the original examination structure while enriching every question with user answers, awarded marks, and evaluation feedback.

---

# Attempt Post-processing

Before evaluation results are stored, the backend performs additional processing depending on the evaluated resource.

### Quiz

* Calculates marks for every question.
* Applies negative marking.
* Calculates:

  * total marks
  * obtained marks
  * percentage
* Stores detailed evaluation for every question.

### Exams

* Merges:

  * original generated examination
  * submitted answers
  * AI evaluation
* Preserves:

  * examination structure
  * blueprint metadata
  * marks
  * question ordering
* Injects:

  * user answers
  * obtained marks
  * AI feedback
* Calculates:

  * section-wise marks
  * overall obtained marks
  * percentage
* Adds overall examination feedback.

---

# Common Error Responses

| Status | Description                                                                                         |
| ------ | --------------------------------------------------------------------------------------------------- |
| 400    | Invalid request body                                                                                |
| 401    | Authentication failed                                                                               |
| 404    | Requested notebook, AI content, or attempt does not exist or is not owned by the authenticated user |
| 422    | Request validation failed                                                                           |
| 429    | Too many requests                                                                                   |
| 500    | Unexpected server error or Database error                                                           |
