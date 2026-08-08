# Notebook API

The Notebook API manages user notebooks.

A notebook acts as the primary container for uploads and AI-generated content. Every notebook belongs to exactly one authenticated user.

All notebook endpoints require authentication.

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

# Endpoints

## Create Notebook

**POST**

```
/v1/notebooks
```

Creates a new notebook for the authenticated user.

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| title | string | Yes | Notebook title |

### Validation

- Minimum length: 1 character
- Maximum length: 100 characters
- Leading and trailing whitespace is removed
- Cannot be empty after trimming

### Success Response

**201 Created**

```json
{
    "success": true,
    "data": {
        "id": "ef81d9b0-cb53-4c1c-bef9-c3c237fd26e4",
        "message": "notebook created"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 400 | Missing JSON body |
| 401 | Missing or invalid access token |
| 422 | Validation error |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

## List Notebooks

**GET**

```
/v1/notebooks
```

Returns all notebooks owned by the authenticated user.

### Query Parameters

| Parameter | Type | Required | Description |
|----------|------|----------|-------------|
| page | integer | No | Page number |
| limit | integer | No | Number of notebooks returned |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "notebooks": [
            {
                "id": "ef81d9b0-cb53-4c1c-bef9-c3c237fd26e4",
                "title": "Operating Systems",
                "created_at": "2026-07-17T10:35:22Z"
            },
            {
                "id": "71fb34d8-4f87-4e0d-b5ea-9c2d21af58b7",
                "title": "Computer Networks",
                "created_at": "2026-07-15T18:21:11Z"
            }
        ]
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid access token |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Get Notebook

**GET**

```
/v1/notebooks/{notebook_id}
```

Returns a single notebook owned by the authenticated user.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "id": "ef81d9b0-cb53-4c1c-bef9-c3c237fd26e4",
        "title": "Operating Systems"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid access token |
| 404 | Notebook not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Edit Notebook

**PATCH**

```
/v1/notebooks/{notebook_id}
```

Updates the title of an existing notebook.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Request Body

| Field | Type | Required | Description |
|------|------|----------|-------------|
| title | string | Yes | Updated notebook title |

The same validation rules used during notebook creation apply.

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "id": "ef81d9b0-cb53-4c1c-bef9-c3c237fd26e4",
        "message": "notebook updated"
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
| 500 | Internal server error or Database error |

---

## Delete Notebook

**DELETE**

```
/v1/notebooks/{notebook_id}
```

Deletes a notebook owned by the authenticated user.

### Path Parameters

| Parameter | Description |
|----------|-------------|
| notebook_id | Notebook UUID |

### Success Response

**204 No Content**

The endpoint returns an empty response body.

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid access token |
| 404 | Notebook not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error or Database error |

---

# Common Error Responses

| Status | Description |
|--------|-------------|
| 400 | Request does not contain a valid JSON body |
| 401 | Authentication failed |
| 404 | Requested notebook does not exist or is not owned by the authenticated user |
| 422 | Request validation failed |
| 429 | Too many requests |
| 500 | Unexpected server error or Database error |

# Next Steps

Explore [Upload API](Upload.md)