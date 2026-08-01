# Blueprint API

## Overview

The Blueprint API manages reusable **exam generation templates**.

A blueprint defines the structure of an examination, including:

- Exam metadata
- Navigation rules
- Section layout
- Question distribution
- Marking scheme
- Answer formats
- Internal choices
- Shared resources

Blueprints themselves do not contain questions.

Instead, they define the structure that the AI uses during exam generation. During exam generation, the backend combines:

```
Notebook Content
        +
Exam Blueprint
        ↓
AI Exam Generation
        ↓
Generated Exam
        ↓
User Attempts
        ↓
AI Evaluation
```

This separation allows the same notebook to generate multiple exam formats (for example, JEE Main, NEET, or SAT) without changing the uploaded study material.

Blueprints are currently consumed by the **Exam Generation** pipeline. Future AI content types may introduce additional blueprint implementations while remaining independent of the existing exam blueprint schema.

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

# Built-in Blueprints

The backend ships with several built-in exam blueprints.

Built-in blueprints are divided into two categories:

- Public Blueprints
- System Blueprints

---

# Public Blueprints

Public blueprints are discoverable through the Blueprint API and can be used directly for exam generation.

Current public blueprints include:

| Blueprint         | Description                                   |
|-------------------|-----------------------------------------------|
| CAT               | Common Admission Test                         |
| CUET              | Common University Entrance Test               |
| Gaokao            | Chinese National College Entrance Examination |
| JEE Main Paper 1  | Engineering entrance examination              |
| JEE Main Paper 2A | Architecture entrance examination             |
| JEE Main Paper 2B | Planning entrance examination                 |
| NEET UG           | Medical entrance examination                  |
| SAT               | Scholastic Assessment Test                    |

Public blueprints:

- are discoverable through the Blueprint API
- cannot be modified directly
- cannot be deleted
- have no owner (`owner = null`)
- may be copied into a user's own collection

When a public blueprint is copied, the copied version becomes a completely independent blueprint owned by the authenticated user.

---

# System Blueprints

The backend also includes several internal system blueprints.

These templates are used by the exam generation pipeline whenever a client does not explicitly provide a blueprint.

Current system blueprints include:

| Blueprint                     | Intended Use                          |
|-------------------------------|---------------------------------------|
| Standard School Exam          | Default school-level examination      |
| Standard University Exam      | Default university-level examination  |
| Standard Competitive Exam     | Default competitive examination       |
| Standard Certification Exam   | Default certification examination     |
| Standard Quiz Exam            | Default lightweight quiz generation   |

System blueprints:

- are not exposed through the Blueprint API
- are not discoverable by users
- cannot be copied
- cannot be modified
- cannot be deleted
- have no owner (`owner = null`)
- are intended solely for internal fallback behavior

When an exam generation request omits a blueprint, the backend automatically selects an appropriate system blueprint for the requested workflow.

---

# Public vs Private Blueprints

Blueprints may be either:

| Visibility | Description                              |
| ---------- | ---------------------------------------- |
| Private    | Visible only to the owner                |
| Public     | Discoverable by every authenticated user |

Public blueprints can be copied into a user's own collection.

The copied blueprint becomes completely independent from the original.

---

# Pagination

Listing endpoints support pagination.

| Parameter | Default | Description                |
| --------- | ------- | -------------------------- |
| page      | 1       | Page number                |
| limit     | 20      | Number of records returned |

The backend enforces a maximum page size configured by the server.

---

# Blueprint Structure

The `structure` field contains the complete exam definition.

```
Blueprint
│
├── exam_name
├── description
├── total_marks
├── duration
├── navigation_rules
│
└── sections
      │
      ├── section_name
      ├── total_marks
      ├── section_duration (optional)
      │
      └── question_groups
              │
              ├── selection_rule
              ├── defaults
              ├── shared_material (optional)
              ├── parts
              └── alternatives
```

---

## Navigation Rules

Navigation rules define how candidates move through the examination.

| Field                          | Description                                           |
| ------------------------------ | ----------------------------------------------------- |
| allow_cross_section_navigation | Whether candidates may switch between sections freely |
| has_sectional_timers           | Enables individual timers for each section            |
| is_computer_adaptive           | Indicates whether the examination is adaptive         |

---

## Sections

An examination consists of one or more sections.

Each section defines:

* section name
* total marks
* optional section duration
* one or more question groups

---

## Question Groups

Question groups describe how questions should be generated.

Every group contains:

* selection rule
* default question configuration
* question distribution
* optional shared material

---

### Selection Rules

Blueprints support multiple selection strategies.

| Rule     | Description                                  |
| -------- | -------------------------------------------- |
| all      | Every generated question appears in the exam |
| or       | Student attempts exactly one alternative     |
| choose_n | Student chooses any N questions              |

---

### Parts

Most question groups use **parts**.

Each part defines:

* question label
* number of questions
* marks per question

Example:

```
Q1-Q10
10 Questions
2 Marks Each
```

---

### Alternatives

Alternative groups model internal choices.

Example:

```
Attempt Any One

Question 18

OR

Question 19
```

Alternative groups are only valid when the selection rule is `or`.

---

### Shared Material

Some question groups generate common material shared by multiple questions.

Supported resource types include:

* Passage
* ASCII Table
* ASCII Diagram

This is typically used for:

* Reading comprehension
* Case studies
* Shared datasets
* Diagram-based questions

---

### Question Defaults

Every question group defines a default configuration inherited by every generated question.

Defaults specify:

* Question type
* Expected answer type
* Negative marking

Supported question types include:

* MCQ
* Multi Select
* Numerical
* True / False
* Fill in the Blank
* Subjective
* Short Subjective
* Diagram Question
* Custom

Supported answer types include:

* single_choice
* multiple_choice
* numeric
* boolean
* text
* essay
* drawing

The backend validates every question type against its compatible answer type.

---

# Example Blueprint

The following example demonstrates every major blueprint feature supported by the backend.

```json
{
  "is_public": true,
  "structure": {
    "exam_name": "Blueprint example",
    "description": "Example blueprint to demonstrate every major blueprint feature supported by backend.",
    "total_marks": 100,
    "duration": "3 hours",
    "navigation_rules": {
      "allow_cross_section_navigation": true,
      "has_sectional_timers": false,
      "is_computer_adaptive": false
    },
    "sections": [
      {
        "section_name": "Fundamentals",
        "total_marks": 20,
        "question_groups": [
          {
            "group_title": "Short Questions",
            "selection_rule": {
              "type": "all"
            },
            "defaults": {
              "question_type": "Subjective_Short",
              "answer_type": "text",
              "negative_marking": 0
            },
            "parts": [
              {
                "label": "Q1-Q10",
                "count": 10,
                "marks": 2
              }
            ]
          }
        ]
      },
      {
        "section_name": "Case Study",
        "total_marks": 40,
        "question_groups": [
          {
            "group_title": "Passage Based Questions",
            "selection_rule": {
              "type": "all"
            },
            "shared_material": {
              "type": "passage"
            },
            "defaults": {
              "question_type": "Subjective",
              "answer_type": "essay",
              "negative_marking": 0
            },
            "parts": [
              {
                "label": "Q11-Q12",
                "count": 2,
                "marks": 10
              }
            ]
          },
          {
            "group_title": "Attempt Any One",
            "selection_rule": {
              "type": "or"
            },
            "defaults": {
              "question_type": "Subjective",
              "answer_type": "essay",
              "negative_marking": 0
            },
            "alternatives": [
              {
                "title": "Question 13",
                "parts": [
                  {
                    "label": "Q13",
                    "count": 1,
                    "marks": 20
                  }
                ]
              },
              {
                "title": "Question 14",
                "parts": [
                  {
                    "label": "Q14",
                    "count": 1,
                    "marks": 20
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

---

# Validation

Blueprints undergo extensive validation before being saved.

Validation includes:

* Total exam marks equal the sum of section marks.
* Section marks equal the sum of all question group marks.
* Question types are compatible with answer types.
* OR groups contain at least two alternatives.
* Non-OR groups must define parts.
* Section timers are required when sectional timing is enabled.
* `choose_n` requires a selection count.
* Negative marking cannot be negative.

Validation failures return:

```
422 Unprocessable Entity
```

along with detailed validation errors.

---

# Endpoints

## Create Blueprint

**POST**

```
/v1/blueprints
```

Creates a new blueprint owned by the authenticated user.

### Request Body

| Field     | Type    | Required | Description                                    |
| --------- | ------- | -------- | ---------------------------------------------- |
| is_public | boolean | No       | Whether the blueprint is publicly discoverable |
| structure | object  | Yes      | Blueprint definition                           |

The `structure` field must conform to the Blueprint Schema.

### Success Response

**201 Created**

```json
{
    "success": true,
    "data": {
        "blueprint_slug": "jee-main-mock-test",
        "message": "Blueprint created successfully"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                                  |
| ------ | --------------------------------------- |
| 400    | Missing JSON body                       |
| 401    | Missing or invalid access token         |
| 422    | Validation error                        |
| 429    | Rate limit exceeded                     |
| 500    | Internal server error or Database error |

---

## List Public Blueprints

**GET**

```
/v1/blueprints
```

Returns all publicly available blueprints.

### Query Parameters

| Parameter | Type    | Required | Description                            |
| --------- | ------- | -------- | -------------------------------------- |
| keyword   | string  | No       | Search blueprint title and description |
| page      | integer | No       | Page number                            |
| limit     | integer | No       | Number of blueprints returned          |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "blueprints": [
            {
                "id": "...",
                "slug": "jee-main-mock-test",
                "name": "JEE Main Mock Test",
                "description": "Standard engineering entrance exam blueprint.",
                "is_public": true,
                "owner": null,
                "created_at": "2026-08-01T12:00:00Z"
            }
        ]
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                          |
| ------ | ------------------------------- |
| 400    | Invalid pagination parameters   |
| 401    | Missing or invalid access token |
| 429    | Rate limit exceeded             |
| 500    | Internal server error           |

---

## List User Blueprints

**GET**

```
/v1/blueprints/me
```

Returns every blueprint owned by the authenticated user.

### Query Parameters

| Parameter | Type    | Required | Description                            |
| --------- | ------- | -------- | -------------------------------------- |
| keyword   | string  | No       | Search blueprint title and description |
| page      | integer | No       | Page number                            |
| limit     | integer | No       | Number of blueprints returned          |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "blueprints": [
            {
                "id": "...",
                "slug": "my-blueprint",
                "name": "My Blueprint",
                "description": "Personal exam template.",
                "is_public": false,
                "owner": "me",
                "created_at": "2026-08-01T12:00:00Z"
            }
        ]
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                          |
| ------ | ------------------------------- |
| 400    | Invalid pagination parameters   |
| 401    | Missing or invalid access token |
| 429    | Rate limit exceeded             |
| 500    | Internal server error           |

---

## Get Blueprint

**GET**

```
/v1/blueprints/{slug}
```

Returns a single blueprint.

Users may retrieve:

* their own private blueprints
* any public blueprint

### Path Parameters

| Parameter | Description    |
| --------- | -------------- |
| slug      | Blueprint slug |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "id": "...",
        "slug": "jee-main-mock-test",
        "name": "JEE Main Mock Test",
        "description": "Standard engineering entrance exam blueprint.",
        "is_public": true,
        "owner": null,
        "created_at": "2026-08-01T12:00:00Z",
        "structure": { ... }
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                          |
| ------ | ------------------------------- |
| 401    | Missing or invalid access token |
| 404    | Blueprint not found             |
| 429    | Rate limit exceeded             |
| 500    | Internal server error           |

---

## Save Public Blueprint

**POST**

```
/v1/blueprints/{slug}/save
```

Creates a private copy of a public blueprint inside the authenticated user's collection.

The original blueprint is not modified.

### Path Parameters

| Parameter | Description           |
| --------- | --------------------- |
| slug      | Public blueprint slug |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "blueprint_slug": "jee-main-mock-test-copy",
        "message": "Blueprint saved successfully"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                                        |
| ------ | --------------------------------------------- |
| 401    | Missing or invalid access token               |
| 404    | Blueprint not found                           |
| 409    | Blueprint already exists in user's collection |
| 429    | Rate limit exceeded                           |
| 500    | Internal server error or database error       |

---

## Edit Blueprint

**PATCH**

```
/v1/blueprints/{slug}
```

Updates an existing blueprint owned by the authenticated user.

### Path Parameters

| Parameter | Description    |
| --------- | -------------- |
| slug      | Blueprint slug |

### Request Body

| Field     | Type    | Required | Description                                    |
| --------- | ------- | -------- | ---------------------------------------------- |
| is_public | boolean | No       | Whether the blueprint is publicly discoverable |
| structure | object  | Yes      | Updated blueprint definition                   |

The updated structure must satisfy the Blueprint Schema.

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "blueprint_slug": "jee-main-mock-test",
        "message": "Blueprint edited successfully"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                                  |
| ------ | --------------------------------------- |
| 400    | Missing JSON body                       |
| 401    | Missing or invalid access token         |
| 404    | Blueprint not found                     |
| 422    | Validation error                        |
| 429    | Rate limit exceeded                     |
| 500    | Internal server error or Database error |

---

## Delete Blueprint

**DELETE**

```
/v1/blueprints/{slug}
```

Deletes a blueprint owned by the authenticated user.

Default system blueprints cannot be deleted.

### Path Parameters

| Parameter | Description    |
| --------- | -------------- |
| slug      | Blueprint slug |

### Success Response

**204 No Content**

The endpoint returns an empty response body.

### Possible Errors

| Status | Reason                                  |
| ------ | --------------------------------------- |
| 401    | Missing or invalid access token         |
| 404    | Blueprint not found                     |
| 429    | Rate limit exceeded                     |
| 500    | Internal server error or Database error |

---

# Blueprint Schema

A blueprint consists of:

* Exam metadata
* Navigation rules
* One or more sections
* Question groups
* Question defaults
* Selection rules
* Alternative question sets
* Shared materials

The request validator performs structural validation including:

* Question type and answer type compatibility
* Section mark consistency
* Overall exam mark consistency
* Alternative question group validation
* Section timer requirements
* Selection rule validation

Requests that violate these rules return:

```
422 Unprocessable Entity
```

with detailed validation errors.

---

# Common Error Responses

| Status | Description                                                             |
| ------ | ----------------------------------------------------------------------- |
| 400    | Request does not contain a valid JSON body or invalid pagination values |
| 401    | Authentication failed                                                   |
| 404    | Requested blueprint does not exist or is not accessible                 |
| 409    | Blueprint already exists in user's collection                           |
| 422    | Request validation failed                                               |
| 429    | Too many requests                                                       |
| 500    | Unexpected server error or Database error                               |
