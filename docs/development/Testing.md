# Testing

## Overview

The project uses a feature-oriented testing architecture designed to support both synchronous and asynchronous execution while keeping tests deterministic, isolated, and easy to extend.

The testing infrastructure separates reusable utilities from feature-specific tests and provides a consistent environment for database setup, Celery workers, fixtures, and resource management.

The overall structure follows the same layered organization used throughout the backend.

```
tests/
├── infrastructure/
├── fixtures/
├── builders/
├── features/
├── resources/
├── _helpers/
└── fakes/
```

---

# Test Architecture

The testing package is divided into several responsibilities.

## infrastructure/

Contains the shared testing environment.

Responsibilities include:

- Flask application creation
- Test database session management
- Celery configuration
- Celery worker startup
- Celery worker cleanup
- Test profile selection

This package ensures every test starts with a clean and reproducible environment.

---

## fixtures/

Fixtures create reusable domain objects used across multiple feature tests.

Examples include:

- users
- notebooks
- uploads
- AI content
- attempts
- blueprints

Fixtures avoid repetitive setup logic while keeping tests readable.

---

## builders/

Builders generate request payloads and test objects.

Unlike fixtures, builders are primarily responsible for constructing customizable input data.

Examples include:

- authentication payloads
- notebook creation requests
- upload requests
- blueprint payloads
- AI generation payloads

Builders make it easy to modify only the fields relevant to a specific test.

---

## features/

Feature tests are organized by business capability.

Each feature contains its own independent test module.

Current feature coverage includes:

- Authentication
- Notebooks
- Uploads
- AI Content
- Attempts
- Blueprints
- Retrieval
- File Processing

This organization mirrors the application architecture and makes new features straightforward to test.

---

## resources/

Contains static files used during testing.

Resources include:

- sample PDFs
- DOCX documents
- Markdown files
- CSV files
- images
- upload fixtures
- blueprint JSON files

Keeping resources centralized allows deterministic testing of document processing.

---

## fakes/

Contains lightweight implementations used during testing.

Examples include:

- fake YouTube transcript extraction

Fake implementations remove external dependencies while keeping behavior predictable.

---

## _helpers/

Shared helper utilities that simplify common testing tasks.

Examples include:

- database assertions
- polling utilities
- Celery worker helpers
- exam answer generation

These helpers keep feature tests focused on behavior rather than implementation details.

---

# Test Environment

The test suite requires the infrastructure services to be running before executing any tests.

Start the required Docker services:

```bash
docker compose -f docker/compose.yaml up -d
```

After the test session is complete, stop the services with:

```bash
docker compose -f docker/compose.yaml down
```

To also remove the PostgreSQL and Redis volumes:

```bash
docker compose -f docker/compose.yaml down -v
```

---

# Running Tests

Run the complete test suite:

```bash
pytest tests
```

or

```bash
python -m pytest tests
```

Run a single feature:

```bash
pytest tests/features/uploads
```

or

```bash
python -m pytest tests/features/uploads
```

Run an individual test:

```bash
pytest tests/features/uploads/test_uploads.py
```

or

```bash
python -m pytest tests/features/uploads/test_uploads.py
```

---

# Synchronous vs Asynchronous Execution

By default, the test suite executes Celery tasks synchronously using eager mode.

This provides:

- deterministic execution
- faster feedback
- simpler debugging
- no background worker requirement

For integration testing, the suite can also execute against a real Celery worker.

Enable asynchronous execution with:

```bash
pytest tests --async_tasks
```

or

```bash
python -m pytest tests --async_tasks
```

When enabled, the testing infrastructure automatically starts the required Celery worker, executes tasks asynchronously, and performs worker cleanup after the test session completes.

This mode validates the real background processing pipeline without changing the test implementations.

---

# Celery Test Infrastructure

The testing infrastructure manages the complete Celery lifecycle.

It is responsible for:

- configuring Celery for the selected execution mode
- starting a dedicated worker for asynchronous tests
- monitoring worker readiness
- shutting the worker down after testing
- cleaning temporary worker resources

Feature tests do not interact with Celery directly.

---

# Test Resources

The testing suite includes reusable resource files covering every supported upload type.

Current resources include:

- PDF
- DOCX
- Markdown
- CSV
- Images
- Plain text
- Blueprint JSON
- Multiple upload samples
- Invalid upload samples

These resources provide stable regression coverage for document processing.

---

# Test Profiles

The infrastructure supports multiple execution profiles.

The selected profile configures:

- database behavior
- Celery execution mode
- cleanup strategy
- session management

Profiles are managed internally by the testing infrastructure and require no modification by feature tests.

---

# Design Principles

The testing architecture follows several core principles.

- Feature tests remain independent.
- Common setup belongs in fixtures or builders.
- Infrastructure handles application lifecycle management.
- External services are replaced with deterministic fakes whenever possible.
- Static resources remain version-controlled.
- Test data construction is separated from assertions.
- Synchronous and asynchronous execution share the same test code.

---

# RAG Evaluation

Retrieval-Augmented Generation (RAG) evaluation is maintained separately from the application test suite.

See:

[rag_evaluation/README.md](../../rag_evaluation/README.md)

for dataset preparation, evaluation metrics, reporting, and execution details.

# Related Documents

- [Project Structure](ProjectStructure.md)
- [Coding Standards](CodingStandards.md)
- [Quick Start](../../QuickStart.md)