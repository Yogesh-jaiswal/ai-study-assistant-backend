# Environment Configuration

## Overview

The backend uses environment variables to configure application behavior across different execution environments.

Configuration is centralized in a single Pydantic settings object. Environment-specific behavior is implemented by applying small override sets on top of the base configuration rather than maintaining multiple independent configuration files.

This approach keeps configuration consistent while avoiding duplicated settings.

---

# Configuration Loading

Application settings are loaded during startup.

The loading process is:

```
Load .env
↓
Create base settings
↓
Determine ENVIRONMENT
↓
Apply environment overrides
↓
Validate configuration
↓
Application startup
```

If validation fails, the application terminates immediately with a descriptive error.

---

# Environment Files

The repository provides an example configuration file:

```
.env.example
```

Copy it before running the project:

```bash
cp .env.example .env
```

Testing uses a separate configuration file:

```
.env.testing
```

This file is primarily intended for automated testing.

---

# Supported Environments

The backend currently supports four execution environments.

## Development

Default environment used during local development.

Characteristics:

- Debug mode enabled
- Verbose logging
- Gemini AI enabled
- Docker service hostnames
- Manual background workers

---

## Testing

Designed for automated test execution.

Overrides include:

- Fake AI provider
- Rate limiting disabled
- Eager Celery execution
- Temporary upload directory
- Localhost database and Redis

The testing environment prioritizes deterministic execution and fast feedback.

---

## Evaluation

Used for RAG evaluation.

Characteristics include:

- Eager Celery execution
- Reduced logging
- Localhost database and Redis

Evaluation focuses on reproducible benchmarking rather than application serving.

---

## Production

Production enables deployment-oriented defaults.

Examples include:

- Debug disabled
- INFO logging
- Redis-backed rate limiting
- Production database
- Gemini AI

Production assumes external infrastructure is already available.

---

# Configuration Categories

Configuration values are grouped by responsibility.

Current categories include:

- Application
- AI provider
- Legacy Quiz generation
- Legacy Notes
- Rate limiting
- Database
- Uploads
- JWT authentication
- Redis
- Celery
- Embeddings
- Retrieval
- Pagination

Grouping related settings keeps configuration easier to maintain as the project grows.

---

# Computed Configuration

Some configuration values are derived automatically.

Examples include:

- Database connection URL
- Redis URL
- JWT private key
- JWT public key

These values are generated from the underlying configuration instead of requiring duplicate environment variables.

---

# Validation

Configuration validation occurs during application startup.

Examples include:

- Required API keys
- Numeric limits
- Supported environment names
- Allowed AI providers
- Valid legacy quiz difficulty values

If validation fails, the application will not start.

This prevents partially configured deployments from running.

---

# Sensitive Configuration

Sensitive values should never be committed to version control.

Examples include:

- API keys
- Database passwords
- JWT private keys
- JWT public keys

The repository includes a `.env.example` file containing placeholder values for local setup.

---

# Environment Overrides

Only settings that differ between environments are overridden.

For example:

Development

```python
DEBUG = True
LOG_LEVEL = "DEBUG"
```

Production

```python
DEBUG = False
LOG_LEVEL = "INFO"
```

This approach minimizes duplicated configuration while keeping environment behavior explicit.

---

# Design Principles

The configuration system follows several principles.

- Single source of truth
- Fail fast on invalid configuration
- Minimal environment-specific overrides
- Type-safe configuration
- No duplicated settings
- Environment-independent application code

---

# Related Documents

- [Quick Start](../../QuickStart.md)
- [Docker Deployment](Docker.md)
- [Backend Architecture](../architecture/Backend.md)