# Upload API

The Upload API manages notebook resources such as study notes and reference materials.

Every upload belongs to exactly one notebook owned by an authenticated user.

Uploads are processed asynchronously before becoming available for AI-powered features.

All upload endpoints require authentication.

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

# Upload Processing

Uploads are processed asynchronously after they are accepted.

Possible processing states are:

| Status     | Description                                             |
| ---------- | ------------------------------------------------------- |
| pending    | Upload has been accepted and is waiting to be processed |
| processing | Upload is currently being processed                     |
| completed  | Processing finished successfully                        |
| failed     | Processing failed and extracted content is unavailable  |

Only uploads in the **completed** state are available for AI generation.

Applications should monitor upload progress using the returned `task_id` instead of repeatedly requesting upload resources while processing is still in progress.

---

# Background Task Polling

Uploading a file or YouTube video starts a background processing task.

Successful upload requests return a `task_id` that can be used to monitor processing progress.

Task status is retrieved using the Infrastructure API:

`GET /v1/tasks/{task_id}`


The task status endpoint reports:

- Current execution status
- Task type
- Task result after successful completion
- Error information if the task fails

See the [Infrastructure API](Infrastructure.md#get-task-status) documentation for the complete polling workflow and response format.

---

# Endpoints

## Upload Files

**POST**

```
/v1/notebooks/{notebook_id}/uploads
```

Uploads one or more files into a notebook.

The endpoint immediately accepts the files and starts background processing.

The returned `task_id` should be used to poll the task status endpoint until processing completes.

After the task succeeds, the upload becomes available according to its processing status.

### Path Parameters

| Parameter   | Description   |
| ----------- | ------------- |
| notebook_id | Notebook UUID |

### Query Parameters

| Parameter | Type   | Required | Description                           |
| --------- | ------ | -------- | ------------------------------------- |
| purpose   | string | No       | Upload purpose (`notes`, `reference`) |

If omitted, the default purpose is:

```
notes
```

### Request

Multipart Form Data

| Field | Type   | Required | Description                 |
| ----- | ------ | -------- | --------------------------- |
| files | file[] | Yes      | One or more files to upload |

### Success Response

**201 Created**

```json
{
    "success": true,
    "data": [
        {
            "upload_id": "cbef7eb0-cb0d-4385-9ec7-f5d846d4bbdf",
            "task_id": "7af2f1bb-f7aa-4b58-ae58-442de0d7821b"
        }
    ],
    "error": null
}
```

### Possible Errors

| Status | Reason                                     |
| ------ | ------------------------------------------ |
| 400    | No file uploaded or invalid upload purpose |
| 401    | Missing or invalid access token            |
| 404    | Notebook not found                         |
| 422    | Request validation failed                  |
| 429    | Rate limit exceeded                        |
| 500    | Internal server error or Database error    |

---

## Upload YouTube Video

**POST**

```
/v1/notebooks/{notebook_id}/uploads/youtube
```

Creates an upload from a YouTube video.

The server retrieves the transcript together with basic video metadata and processes it like any other upload.

Videos without publicly available transcripts eventually enter the **failed** processing state.

The returned `task_id` should be used to poll the task status endpoint until transcript extraction and processing complete.

### Path Parameters

| Parameter   | Description   |
| ----------- | ------------- |
| notebook_id | Notebook UUID |

### Request Body

| Field | Type   | Required | Description       |
| ----- | ------ | -------- | ----------------- |
| url   | string | Yes      | YouTube video URL |

Supported hosts:

* youtube.com
* [www.youtube.com](http://www.youtube.com)
* m.youtube.com
* youtu.be

### Success Response

**201 Created**

```json
{
    "success": true,
    "data": {
        "upload_id": "cbef7eb0-cb0d-4385-9ec7-f5d846d4bbdf",
        "task_id": "7af2f1bb-f7aa-4b58-ae58-442de0d7821b"
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                                  |
| ------ | --------------------------------------- |
| 400    | Invalid YouTube URL                     |
| 401    | Missing or invalid access token         |
| 404    | Notebook not found                      |
| 422    | Validation error                        |
| 429    | Rate limit exceeded                     |
| 500    | Internal server error or Database error |

---

## List Uploads

**GET**

```
/v1/notebooks/{notebook_id}/uploads
```

Returns uploads owned by the authenticated user for the specified notebook.

### Path Parameters

| Parameter   | Description   |
| ----------- | ------------- |
| notebook_id | Notebook UUID |

### Query Parameters

| Parameter | Type   | Required | Description                                         |
| --------- | ------ | -------- | --------------------------------------------------- |
| purpose   | string | No       | Upload purpose filter (`notes`, `reference`, `all`) |

When omitted:

```
all
```

is used.

Pagination is supported using the standard `page` and `limit` parameters.

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "uploads": [
            {
                "id": "cbef7eb0-cb0d-4385-9ec7-f5d846d4bbdf",
                "filename": "operating_systems.pdf",
                "source_type": "pdf",
                "upload_purpose": "notes",
                "processing_status": "completed",
                "uploaded_at": "2026-07-20T14:20:18Z"
            }
        ]
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                          |
| ------ | ------------------------------- |
| 400    | Unknown upload purpose          |
| 401    | Missing or invalid access token |
| 404    | Notebook not found              |
| 429    | Rate limit exceeded             |
| 500    | Internal server error           |

---

## Get Upload

**GET**

```
/v1/notebooks/{notebook_id}/uploads/{upload_id}
```

Returns metadata together with the extracted text for a processed upload.

Only uploads whose processing status is **completed** may be retrieved.

### Path Parameters

| Parameter   | Description   |
| ----------- | ------------- |
| notebook_id | Notebook UUID |
| upload_id   | Upload UUID   |

### Success Response

**200 OK**

```json
{
    "success": true,
    "data": {
        "id": "cbef7eb0-cb0d-4385-9ec7-f5d846d4bbdf",
        "filename": "operating_systems.pdf",
        "source_type": "pdf",
        "upload_purpose": "notes",
        "processing_status": "completed",
        "uploaded_at": "2026-07-20T14:20:18Z",
        "raw_text": "..."
    },
    "error": null
}
```

### Possible Errors

| Status | Reason                                                    |
| ------ | --------------------------------------------------------- |
| 401    | Missing or invalid access token                           |
| 404    | Notebook or upload not found                              |
| 409    | Upload processing is still pending, processing, or failed |
| 429    | Rate limit exceeded                                       |
| 500    | Internal server error                                     |

---

## Preview Upload

**GET**

```
/v1/notebooks/{notebook_id}/uploads/{upload_id}/preview
```

Streams the original uploaded resource directly from storage without forcing a download.

Preview is independent of upload processing status because it serves the original uploaded resource rather than extracted content.

### Path Parameters

| Parameter   | Description   |
| ----------- | ------------- |
| notebook_id | Notebook UUID |
| upload_id   | Upload UUID   |

### Success Response

**200 OK**

Returns the uploaded file directly.

### Possible Errors

| Status | Reason                          |
| ------ | ------------------------------- |
| 401    | Missing or invalid access token |
| 404    | Notebook or upload not found    |
| 429    | Rate limit exceeded             |
| 500    | Internal server error           |

---

## Delete Upload

**DELETE**

```
/v1/notebooks/{notebook_id}/uploads/{upload_id}
```

Deletes an upload owned by the authenticated user.

Deleting an upload also removes its extracted content, chunks, embeddings, and local storage file.

### Path Parameters

| Parameter   | Description   |
| ----------- | ------------- |
| notebook_id | Notebook UUID |
| upload_id   | Upload UUID   |

### Success Response

**204 No Content**

The endpoint returns an empty response body.

### Possible Errors

| Status | Reason                                  |
| ------ | --------------------------------------- |
| 401    | Missing or invalid access token         |
| 404    | Notebook or upload not found            |
| 429    | Rate limit exceeded                     |
| 500    | Internal server error or Database error |

---

# Common Error Responses

| Status | Description                                                                                                     |
| ------ | --------------------------------------------------------------------------------------------------------------- |
| 400    | Malformed request or invalid upload purpose                                                                     |
| 401    | Authentication failed                                                                                           |
| 404    | Requested notebook or upload does not exist or is not owned by the authenticated user                           |
| 409    | Requested upload exists but extracted content is unavailable because processing has not completed or has failed |
| 422    | Request validation failed                                                                                       |
| 429    | Too many requests                                                                                               |
| 500    | Unexpected server error or Database error                                                                       |

# Next Steps

Explore [Chat API](Chat.md)