# Infrastructure API

The Infrastructure API exposes backend-wide endpoints that are independent of any specific feature.

These endpoints provide operational capabilities such as health checks and asynchronous task status polling.

---

# Authorization

Only task polling requires authentication.

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

Missing, expired, or invalid access tokens result in:

```
401 Unauthorized
```

The health check endpoint is public.

---

# Endpoints

## Health Check

**GET**

```
/
```

Returns the current health status of the backend.

This endpoint is primarily intended for deployment platforms, monitoring systems, and load balancers to verify that the application is running.

### Success Response

**200 OK**

```json
{
    "message": "AI Study Assistant is running"
}
```

### Possible Errors

The endpoint should always return **200 OK** while the application is running.

---

## Get Task Status

**GET**

```
/v1/tasks/{task_id}
```

Returns the current execution status of an asynchronous background task.

This endpoint is intended to be polled by frontend clients after submitting asynchronous requests such as:

- File uploads
- AI content generation
- Attempt evaluation
- Future asynchronous workflows

### Path Parameters

| Parameter | Description |
|-----------|-------------|
| task_id | Background task UUID |

### Success Response (Pending)

**200 OK**

```json
{
    "success": true,
    "data": {
        "task_id": "...",
        "status": "PENDING",
        "type": "upload"
    },
    "error": null
}
```

### Success Response (Completed)

**200 OK**

```json
{
    "success": true,
    "data": {
        "task_id": "...",
        "status": "SUCCESS",
        "type": "summary_generation",
        "result": {
            "content_id": "..."
        }
    },
    "error": null
}
```

The structure of `result` depends on the task type.

### Failed Task

If the background task fails, the endpoint returns the task information together with the failure reason.

**200 OK**

```json
{
    "success": true,
    "data": {
        "task_id": "...",
        "status": "FAILURE",
        "type": "upload",
        "error": "File not found"
    },
    "error": null
}
```

### Task States

Typical task states include:

| Status | Description |
|--------|-------------|
| PENDING | Task has been queued but has not started |
| STARTED | Task is currently executing |
| RETRY | Task is being retried after a transient failure |
| SUCCESS | Task completed successfully |
| FAILURE | Task failed permanently |

### Possible Errors

| Status | Reason |
|--------|--------|
| 401 | Missing or invalid access token |
| 404 | Task not found or not owned by the authenticated user |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

# Common Error Responses

| Status | Description |
|--------|-------------|
| 401 | Authentication failed |
| 404 | Requested task does not exist or is not owned by the authenticated user |
| 429 | Too many requests |
| 500 | Unexpected server error |