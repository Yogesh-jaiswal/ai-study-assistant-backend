# Backend Architecture

## Overview

The AI Study Assistant backend follows a **Layered Architecture** designed around separation of responsibilities, modularity, and asynchronous processing.

Each layer has a single responsibility and communicates only with its immediate lower layer. This keeps business logic isolated from HTTP handling, persistence, and infrastructure-specific code while making the codebase easier to extend and maintain.

The backend is implemented as a feature-oriented modular monolith. Each feature owns its routes, services, validators, generators, and persistence logic while sharing common infrastructure such as authentication, AI providers, Celery, retrieval, and persistence utilities.

---

## Feature-Oriented Organization

Business features are organized into independent modules.

Each feature owns its own:

* Routes
* Validators
* Services
* Jobs
* Schemas
* AI generators or evaluators
* Persistence logic

Shared infrastructure such as authentication, AI providers, Celery, storage, and retrieval remains centralized and reusable across all features.

---

## Architectural Layers

```
Client
    ↓
Routes
    ↓
Services
    ↓
Repositories
    ↓
Database
```

Each layer exposes functionality to the layer directly above it.

Higher layers should never bypass intermediate layers.

---

## Layer Responsibilities

### Routes

Routes are responsible only for HTTP concerns.

Responsibilities include:

* Request parsing
* Request validation
* Authentication decorators
* Calling services
* Returning standardized API responses

Routes **must not contain business logic**.

---

### Services

Services contain the application's business logic.

Responsibilities include:

* Coordinating workflows
* Calling repositories
* Calling reusable services
* Performing business validations
* Scheduling background jobs
* Coordinating AI features
* Creating execution contexts for asynchronous workflows

The majority of application logic belongs here.

Services may call other services when functionality is shared.

Examples:

* Password hashing
* JWT generation
* AI generators

---

### Repositories

Repositories isolate all database operations.

Responsibilities include:

* CRUD operations
* Query construction
* Database persistence

Repositories do not contain business logic.

They never call services or routes.

---

### Database

The database layer stores all persistent application data.

Current technologies include:

* PostgreSQL
* SQLAlchemy ORM
* pgvector (vector search)

---

## Background Processing

Operations that are computationally expensive or time-consuming execute asynchronously through Celery.

Examples include:

* File processing
* Chunk generation
* Embedding generation
* AI content generation

Typical workflow:

```
Route
    ↓
Service
    ↓
Validator
    ↓
Celery Task
    ↓
Loader
    ↓
Bundle
    ↓
Job
    ↓
Repository
```

Background tasks reuse existing services whenever possible instead of implementing duplicate business logic.

---

## Middleware

The backend uses global Flask middleware to perform request lifecycle operations that are independent of business logic.

Current middleware responsibilities include:

- Assigning a unique request ID for traceability.
- Recording request start time.
- Measuring total request duration.
- Logging request lifecycle events.
- Logging unhandled exceptions during request teardown.

Middleware operates entirely outside the service layer and does not contain business logic.

Typical request flow:

```
Client
↓
Before Request Middleware
↓
Route
↓
Service
↓
Repository
↓
After Request Middleware
↓
Response
```

---

## Dependency Rules

The backend follows strict dependency rules.

Allowed dependencies:

```
Routes
    ↓
Services
    ↓
Repositories
    ↓
Database
```

Additional rules:

* Services may call reusable services.
* Celery tasks may call services and repositories.
* Tests may access all layers.
* Configuration is accessible throughout the application.
* Logging is available throughout the application.
* Error handlers remain independent and may catch exceptions from any layer.
* Route decorators are only used within the routing layer.

---

## Feature Jobs

Feature Jobs provide an orchestration layer between asynchronous Celery tasks and feature-specific workflows.

Responsibilities include:
* Executing feature workflows
* Receiving fully prepared bundles
* Coordinating generators or evaluators
* Performing feature-specific post-processing
* Preparing persistence objects

Feature Jobs allow Celery workers to remain generic while feature implementations evolve independently.

---

## Design Principles

### Thin Routes

Routes should remain lightweight.

Business logic belongs in services.

---

### Single Responsibility

Every layer has one clearly defined purpose.

Responsibilities should not overlap.

---

### Separation of Concerns

Business logic, persistence, HTTP handling, AI integration, and background execution remain isolated from one another.

---

### Reusability

Reusable functionality should exist once and be shared throughout the application.

Examples include:

* Authentication helpers
* AI infrastructure
* Generation Bundles
* Evaluation Bundles
* File processing pipeline
* Retrieval pipeline

---

### Modularity

New features should be implemented by extending the architecture instead of modifying unrelated modules.

Examples include:

* New AI generators and generation workflows
* New retrieval strategies
* New file processors
* Additional AI providers
* New asynchronous feature workflows

---

## What the Backend Does Not Handle

The backend intentionally avoids frontend responsibilities.

These include:

* UI rendering
* Visual presentation
* Client-side state management
* Interactive diagrams
* Frontend visualization

The backend exposes APIs and structured data while leaving rendering to frontend clients.

---

## Scalability Vision

Although the project is currently a learning-focused backend, the architecture is designed with production-oriented principles.

Long-term goals include:

* Easily extendable feature modules
* Minimal coupling between components
* Support for asynchronous workloads
* Low-latency request handling
* Horizontal scalability
* Minimal refactoring when introducing new AI features or providers

The emphasis is on writing maintainable software rather than optimizing prematurely.

---

## Related Architecture Documents

* [Authentication Architecture](authentication.md)
* [AI Architecture](ai.md)
* [Attempt Architecture](attempts.md)
* [Retrieval Architecture](retrieval.md)
* [Database Architecture](database.md)
* [Celery Architecture](celery.md)
* [File Processing Architecture](file_processing.md)