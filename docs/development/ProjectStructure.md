# Project Structure

## Overview

The AI Study Assistant backend follows a feature-oriented modular structure built around clear separation of responsibilities. Each package has a well-defined purpose, making the codebase easier to navigate, extend, and maintain.

Business logic, infrastructure, persistence, background processing, testing, and documentation are organized into dedicated directories to minimize coupling and encourage consistency across the project.

Rather than grouping code by file type alone, related functionality is organized into cohesive feature modules while shared infrastructure remains centralized.

---

# Top-Level Structure

The project is organized into the following major directories.

```text
app/
configs/
decorators/
docker/
docs/
handlers/
middlewares/
migrations/
models/
repositories/
resources/
routes/
services/
tasks/
tests/
utils/
validators/
```

Each directory has a single primary responsibility.

---

# Core Application

## app/

Contains the application bootstrap and initialization logic.

Responsibilities include:

- Flask application factory
- Celery application configuration
- extension initialization
- application startup
- CLI commands
- JWT key management

This package is responsible for creating the application instance and wiring together the shared infrastructure.

---

## configs/

Contains the application's configuration system.

Responsibilities include:

- environment-specific configuration
- logging configuration
- rate limiting configuration
- settings validation
- configuration overrides

The backend supports multiple execution environments while exposing a unified settings object throughout the application.

---

## routes/

Contains every HTTP endpoint exposed by the backend.

Routes are organized by feature and remain responsible only for:

- request parsing
- request validation
- authentication
- calling services
- returning standardized responses

Business logic should never be implemented inside routes.

---

## services/

Contains the application's business logic.

This is the largest package in the project and is organized into feature-oriented subpackages.

Examples include:

- authentication
- notebooks
- uploads
- AI generation
- retrieval
- chat
- exams
- quizzes
- flashcards
- file processing
- task status
- AI providers

Specialized orchestration packages are also maintained separately.

Examples include:

- AI generation workflows
- attempt workflows
- asynchronous feature jobs

Keeping services organized by responsibility allows new features to be added with minimal impact on existing functionality.

---

## repositories/

Repositories isolate all database access.

Responsibilities include:

- CRUD operations
- query construction
- persistence
- database lookups

Repositories never contain business logic.

---

## models/

Contains all SQLAlchemy models representing persistent application data.

Examples include:

- users
- notebooks
- uploads
- AI content
- document chunks
- embeddings
- refresh tokens
- attempts

These models define the application's database schema.

---

## validators/

Contains Pydantic request and response schemas.

Responsibilities include:

- request validation
- response validation
- query parameter validation
- feature-specific schemas

Validation remains centralized to keep services focused entirely on business logic.

---

# Background Processing

## tasks/

Contains Celery tasks.

Tasks act as lightweight entry points executed by Celery workers.

Responsibilities include:

- receiving asynchronous requests
- invoking feature workflows
- reporting execution status

Tasks intentionally remain small and delegate actual work to the service layer.

---

## AI Jobs

Feature-specific orchestration is separated from Celery tasks.

Examples include:

- AI generation jobs
- attempt evaluation jobs

These jobs coordinate feature workflows while allowing Celery workers to remain generic and reusable.

---

# Infrastructure

## decorators/

Contains reusable route decorators.

Examples include:

- authentication decorators
- request validation decorators

Decorators encapsulate reusable request-processing behavior.

---

## middlewares/

Contains global request lifecycle middleware.

Examples include:

- request logging
- request timing
- request ID generation

Middleware operates independently of application business logic.

---

## handlers/

Contains centralized exception handlers responsible for converting application exceptions into standardized API responses.

---

## utils/

Contains reusable helper utilities shared across multiple features.

Utilities contain generic functionality that does not naturally belong to a specific business module.

---

# Development Infrastructure

## docker/

Contains everything required for containerized development and deployment.

This includes:

- Dockerfile
- Docker Compose configurations
- PostgreSQL initialization
- container-specific resources

The project intentionally separates infrastructure containers from application containers through multiple Compose files.

Refer to [Docker Deployment](../deployment/Docker.md) for more information.

---

## migrations/

Contains Alembic database migrations.

Database schema changes are version controlled through migration scripts instead of automatic schema generation.

---

## resources/

Contains static resources distributed with the application.

Examples include:

- exam blueprint templates
- bundled configuration resources

These files are part of the application itself rather than user-generated content.

---

# Testing

## tests/

Contains the complete testing infrastructure.

The testing architecture mirrors the application structure while separating reusable testing utilities from feature tests.

Major components include:

- infrastructure
- fixtures
- builders
- feature tests
- helper utilities
- testing resources
- fakes

Additional details are available in the [Testing documentation](Testing.md).

## rag_evaluation/

Contains DeepEval based RAG evaluation module.

Major Components include:
- Corpus
- Setup
- Report
- Evaluation
- State
- Dataset

Additional details are available in the [RAG Evaluation Documenation](../../rag_evaluation/README.md).

---

# Documentation

## docs/

Contains the complete project documentation.

Documentation is organized into multiple categories.

These include:

- Architecture
- API
- Deployment
- Development
- Architectural Decisions

Keeping documentation alongside the source code ensures it evolves together with the project.

---

# Naming Conventions

The project follows consistent naming conventions.

General guidelines include:

- repositories end with `_repository.py`
- services end with `_service.py`
- generators and evaluators remain separate
- schemas are grouped together
- Celery tasks remain inside `tasks/`
- orchestration logic remains inside dedicated job packages
- tests mirror the corresponding application features

These conventions improve discoverability and maintain consistency across the codebase.

---

# Understanding Background Processing

The project separates asynchronous execution into multiple layers.

```
Celery Task
        ↓
Feature Job
        ↓
Business Service
        ↓
Repository
```

Each layer has a different responsibility.

- **Tasks** receive work from Celery.
- **Feature Jobs** coordinate feature-specific workflows.
- **Services** implement business logic.
- **Repositories** interact with the database.

This separation keeps asynchronous execution reusable while preventing duplication of business logic.

---

# Adding a New Feature

Most new features follow the same structure.

```
routes/
        ↓
services/
        ↓
repositories/
        ↓
models/
        ↓
validators/
        ↓
tests/
```

If asynchronous processing is required, the feature may additionally introduce:

- Celery tasks
- feature jobs
- generation or evaluation workflows

Following this structure keeps new functionality consistent with the existing architecture.

---

# Where Should New Code Go?

| If you're adding... | Place it in... |
|---------------------|----------------|
| HTTP endpoint | `routes/` |
| Business logic | `services/` |
| Database access | `repositories/` |
| Database models | `models/` |
| Request or response validation | `validators/` |
| Celery task | `tasks/` |
| Asynchronous workflow orchestration | Feature job packages |
| Shared helper | `utils/` |
| Route decorator | `decorators/` |
| Middleware | `middlewares/` |
| Database migration | `migrations/` |
| Feature tests | `tests/features/` |
| Documentation | `docs/` |

---

# Design Principles

The project structure is guided by several core principles.

- Every package has a single primary responsibility.
- Business logic remains independent of HTTP handling.
- Database access is isolated from application logic.
- Features remain modular and easy to extend.
- Shared infrastructure is centralized and reusable.
- Testing mirrors the application architecture.
- Documentation evolves alongside the implementation.

This organization aims to keep the backend maintainable as new AI capabilities and application features are introduced.

# Related Documents
- [Coding Standards](CodingStandards.md)
- [Testing Guide](Testing.md)
- [Backend Architecture](../architecture/Backend.md)