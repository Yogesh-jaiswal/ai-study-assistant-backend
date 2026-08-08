# Docker Deployment

## Overview

The AI Study Assistant backend uses Docker Compose to provide a reproducible development and deployment environment.

Docker is responsible for running the infrastructure services required by the backend, while keeping the host machine independent of PostgreSQL, Redis, and their configuration.

The Docker setup is intentionally split into multiple Compose files to support different execution scenarios without duplicating configuration.

---

# Directory Structure

```
docker/
├── Dockerfile
├── compose.yaml
├── compose.app.yaml
├── postgres/
│   └── init.sql
```

---

# Docker Components

The Docker environment consists of four services.

## PostgreSQL

Provides the primary relational database.

Features include:

- PostgreSQL 17
- pgvector extension
- automatic database initialization
- persistent storage using Docker volumes
- health checks before dependent services start

The initialization script is executed automatically when the database volume is created for the first time.

### Changing PostgreSQL initialization variables

`POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` are only used during the first database initialization. If you change these values after the database volume has been created, PostgreSQL will continue using the existing credentials. For development, recreate the database volume:

```bash
docker compose -f docker/compose.yaml down  -v
docker compose -f docker/compose.yaml up -d 
```

> [!WARNING]
> This command removes all local PostgreSQL and Redis volumes. Any locally stored data will be lost.

---

## Redis

Redis serves as the application's message broker and cache.

It is used for:

- Celery task queue
- asynchronous communication
- caching (where applicable)

Redis persistence is enabled using append-only files.

---

## Application

The application container runs the Flask backend.

Responsibilities include:

- serving HTTP requests
- executing business logic
- interacting with PostgreSQL
- communicating with Redis
- processing uploaded files

The application waits until both PostgreSQL and Redis become healthy before starting.

---

## Celery Worker

The Celery container executes asynchronous background tasks.

Typical tasks include:

- document processing
- embedding generation
- AI generation workflows
- retrieval preprocessing

---

# Dockerfile

The project uses a single Dockerfile for both the Flask application and the Celery worker.

The image contains:

- Python 3.13
- Tesseract OCR
- English and Hindi OCR language packs
- PostgreSQL client libraries
- build tools required by Python packages
- CPU-only PyTorch
- all Python dependencies

The application source code is copied after dependency installation to maximize Docker layer caching during development.

---

# Compose Files

The project intentionally separates infrastructure services from application services.

## compose.yaml

Contains only the infrastructure required by the backend.

Services:

- PostgreSQL
- Redis

This file is primarily used by:

- automated tests
- RAG evaluation
- local development when only infrastructure is needed

Start infrastructure:

```bash
docker compose -f docker/compose.yaml up -d
```

Stop infrastructure:

```bash
docker compose -f docker/compose.yaml down
```

---

## compose.app.yaml

Extends the base Docker configuration by adding application containers.

Additional services:

- Flask application
- Celery worker

This file depends on compose.yaml and is intended for normal backend execution.

Start the complete backend:

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml \
    up -d
```

Stop the complete backend:

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml \
    down
```

---

# Running Without Docker

Docker is recommended but not mandatory.

Developers may run the backend directly on the host machine by installing:

- PostgreSQL
- Redis

The application configuration can then be updated to point to the locally running services.

This approach is useful for debugging or environments where Docker is unavailable.

---

# Docker Layer Caching

The Dockerfile is organized to maximize layer reuse.

Dependency installation occurs before the application source code is copied.

As a result:

- changing Python source files usually rebuilds only the final image layer
- dependency installation is reused whenever `requirements.txt` remains unchanged

This significantly reduces rebuild time during development.

---

# Hugging Face Model Caching

Sentence Transformer models are **not** bundled into the Docker image.

Instead, the model is downloaded automatically the first time the application starts.

The downloaded model is stored inside Hugging Face's cache.

Subsequent container starts reuse the cached model instead of downloading it again, reducing startup time and network usage.

No manual model installation is required.

---

# OCR Support

The Docker image includes Tesseract OCR.

Installed language packs include:

- English
- Hindi

Additional languages can be installed by extending the Dockerfile with the corresponding Tesseract language packages.

---

# Troubleshooting

## Redis or PostgreSQL connection failures

Verify the infrastructure services are running:

```bash
docker compose -f docker/compose.yaml ps
```

---

## View application logs

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml \
    logs app
```

View Celery logs:

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml \
    logs celery
```

---

## Rebuild images

If dependencies or the Dockerfile change:

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml \
    build
```

---

## Remove all containers and volumes

To completely reset the Docker environment:

```bash
docker compose \
    -f docker/compose.yaml \
    -f docker/compose.app.yaml \
    down -v
```

This removes all containers and persistent Docker volumes.

Database contents will be lost.

---

# Design Principles

The Docker setup follows several principles.

- Infrastructure is separated from application services.
- Development, testing, and evaluation share the same infrastructure configuration.
- Containers start only after required dependencies become healthy.
- Persistent application data survives container recreation.
- Docker layer caching minimizes rebuild time.
- The same Docker image is reused for both the Flask application and Celery workers.

# Related Documents

- [Environment Setup](Environment.md)
- [Backend Architecture](../architecture/Backend.md)
- [Quick Start](../../QuickStart.md)