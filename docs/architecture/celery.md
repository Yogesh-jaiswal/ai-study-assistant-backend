# Celery Architecture

## Overview

The backend uses **Celery** to execute long-running and computationally expensive operations asynchronously.

Typical asynchronous workloads include:

- File processing
- Chunk generation
- Embedding generation
- AI content generation
- AI content evaluation

Celery allows HTTP requests to return immediately while background workers continue processing independently.

---

## Design Goals

The Celery architecture was designed around the following principles:

- Keep HTTP requests short-lived.
- Execute expensive work asynchronously.
- Reuse existing business logic whenever possible.
- Support both synchronous and asynchronous execution during testing.
- Retry transient infrastructure failures automatically.
- Keep Celery-specific code isolated from business features.

---

## Architecture

```
Request
   ↓
Validation
   ↓
Enqueue Celery Task
   ↓
Background Processing
   ↓
Task Status API
   ↓
Client Receives Result
```

Routes never dispatch Celery tasks directly.

Services decide whether background execution is required and enqueue the appropriate task.

---

## Components

### Celery Application

The Celery application configures:

- Redis broker
- Redis result backend
- Task execution mode
- Imported task modules

It contains no business logic.

---

### Worker Bootstrap

Celery workers execute independently from the Flask application.

A dedicated worker bootstrap creates the Flask application and injects the application context into every Celery task.

```
Worker
    ↓
Create Flask App
    ↓
Inject App Context
    ↓
Execute Task
```

This allows tasks to access:

- SQLAlchemy
- Configuration
- Extensions
- Repositories
- Services

without manually creating an application context.

---

### Tasks

Tasks are the entry point for asynchronous execution.

Their responsibilities include:

- Coordinating long-running workflows
- Calling services and repositories
- Managing retries
- Returning task results

Tasks intentionally avoid implementing reusable business logic.

Instead, they orchestrate existing components.

Examples include:

- Processing uploaded files
- Creating AI-generated content
- Evaluating AI-generated content

---

## Task Workflows

Different workloads may have different internal workflows.

### File Processing

```
Route
    ↓
Creation Service
    ↓
Celery Task
        ↓
    Extract Text
        ↓
    Chunk Content
        ↓
 Generate Embeddings
        ↓
  Persist Results
```

### AI Content Generation

```
Route
    ↓
Creation Service
    ↓
Celery Task
    ↓
Generation Validator
    ↓
Generation Loader
    ↓
Generation Bundle
    ↓
Generation Job
    ↓
Feature Generator
    ↓
AI Engine
    ↓
Provider
    ↓
Persist AI Content
```

### AI Content Evaluation

```
Route
    ↓
Attempt Service
    ↓
Celery Task
    ↓
Attempt Loader
    ↓
Evaluation Bundle
    ↓
Attempt Job
    ↓
Feature Evaluator
    ↓
AI Engine (when required)
    ↓
Provider
    ↓
Persist Attempt
```

Celery itself is unaware of business-specific workflows.

Generation and evaluation each define their own orchestration pipeline while sharing the same asynchronous execution infrastructure.

Each task coordinates the workflow appropriate for its domain.

---

## Retry Strategy

Tasks automatically retry transient infrastructure failures.

Current retry policy includes:

- Redis connection failures
- Redis timeout failures

Configuration:

- Exponential backoff
- Maximum of three retries

Business validation failures are **not retried**, since they are deterministic and cannot succeed on subsequent attempts.

---

## Task Ownership

Services enqueue tasks and remain responsible for business validation.

Typical validations performed before dispatching include:

- Notebook ownership validation
- Upload existence checks
- Processing status validation

Once validation succeeds, the service dispatches the task.

This prevents invalid work from entering the queue.

---

## Task Status Tracking

Every background task returns a task identifier immediately after being enqueued.

Clients can use this identifier to poll a dedicated task status endpoint.

Typical workflow:

```
Client
    ↓
Submit Request
    ↓
Receive Task ID
    ↓
Poll Task Status
    ↓
Receive Final Result
```

A task may be in one of several states, including:

- Pending
- Started
- Success
- Failure
- Retry

When a task completes successfully, it may return task-specific metadata.

Examples include:

File processing:

```json
{
    "upload_id": "...",
    "file_status": "completed"
}
```

AI content generation:

```json
{
    "content_id": "..."
}
```

Attempt evaluation

```json
{
    "attempt_id": "...",
    "attempt_status": "completed"
}
```

Task ownership is also stored to ensure that only the user who created the task can retrieve its status or result.

This mechanism provides asynchronous progress tracking without requiring long-lived HTTP connections.

---

## Testing

The architecture supports both synchronous and asynchronous task execution during testing.

### Default Mode

By default, Celery runs in **eager mode**, where tasks execute immediately inside the current process.

```
Route
    ↓
Service
    ↓
Celery
    ↓
Task executes immediately
```

This provides:

- Deterministic tests
- No running worker required
- Simpler debugging

### Async Mode

When running tests with the `--async-tasks` flag, tasks execute through a real Celery worker.

This allows testing:

- Celery worker configuration
- Redis integration
- Task serialization
- Retry behavior
- End-to-end asynchronous workflows

The same task implementation is used in both testing modes and production.

---

## Queues

The current architecture uses a single default queue.

All background tasks share this queue.

Future versions may introduce dedicated queues for different workloads, for example:

- File processing
- AI generation
- Scheduled maintenance

This optimization is deferred until workload characteristics justify queue separation.

---

## Design Principles

### Tasks are orchestration units

Tasks coordinate asynchronous workflows.

Reusable business logic belongs in services.

---

### Services own validation

Tasks assume that the request has already passed business validation.

Services prevent invalid work from entering the queue.

---

### Background execution is transparent

Business features should not know whether work executes synchronously or asynchronously.

Only the service decides when background execution is appropriate.

---

### Reuse existing layers

Tasks reuse repositories and services rather than duplicating logic.

This keeps asynchronous and synchronous execution paths consistent.

---

## Future Improvements

Potential improvements include:

- Multiple queues
- Task priorities
- Scheduled jobs
- Dead-letter queues
- Chained task workflows
- Distributed workers
- Worker autoscaling
- Queue metrics and monitoring
- Auto cleanup tasks (for example, refresh token cleanup and other periodic maintenance jobs)

---

## Guiding Principle

Celery is an execution mechanism rather than a business layer.

Business logic belongs in services.

Celery tasks coordinate asynchronous workflows while reusing the existing application architecture.