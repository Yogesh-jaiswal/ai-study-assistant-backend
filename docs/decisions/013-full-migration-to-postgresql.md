# Decision 013: Full Migration to PostgreSQL

## Decision

Migrate the backend from a hybrid SQLite/PostgreSQL architecture to a PostgreSQL-only architecture across all environments.

SQLite is no longer supported as an application database.

## Reason

During Phase 5, the project reached a point where maintaining multiple database implementations provided little benefit while increasing development and operational complexity.

Several new backend capabilities depend directly on PostgreSQL:

* Native pgvector support for semantic search
* Production-grade vector indexing
* Advanced PostgreSQL extensions
* Consistent schema management across environments

Maintaining SQLite alongside PostgreSQL introduced duplicated effort in configuration, testing, and infrastructure while providing no long-term architectural advantage.

Using PostgreSQL everywhere simplifies both development and production while aligning the project with its future AI infrastructure.

## Current Behavior

The backend now uses PostgreSQL exclusively for every environment.

* Development uses PostgreSQL.
* Testing uses PostgreSQL.
* Production uses PostgreSQL.
* Database schema is managed through Alembic migrations.
* pgvector can be enabled without requiring a future database migration.

Separate databases are created for each environment:

* ai_study_assistant
* ai_study_assistant_test
* ai_study_assistant_prod

This provides complete isolation while keeping every environment on the same database engine.

## Benefits

The migration provides several architectural benefits:

* Single database implementation to maintain.
* Full compatibility with pgvector for semantic retrieval.
* Elimination of SQLite-specific code paths.
* Identical behavior across development, testing, and production.
* Simplified Docker and CI configuration.
* Reduced maintenance of search and storage infrastructure.
* Easier future optimization using PostgreSQL extensions.

## Consequences

### Positive

* One relational database technology across the entire project.
* No future SQLite ↔ PostgreSQL migration required.
* Lower maintenance burden.
* Cleaner configuration and deployment.
* Better alignment with future AI and RAG features.

### Negative

* PostgreSQL becomes a mandatory development dependency.
* Local development now requires a running PostgreSQL instance (or Docker Compose).

These trade-offs are acceptable because PostgreSQL is already required for production deployment and vector search.

## Future Revisit Criteria

Reconsider this decision only if:

* A lightweight embedded deployment becomes a product requirement.
* Offline desktop deployments require an embedded database.
* A future storage architecture replaces PostgreSQL entirely.

No migration back to SQLite is currently planned.

## Implementation Notes

The migration includes:

* Removal of SQLite-specific configuration.
* PostgreSQL as the default database backend.
* Environment-specific PostgreSQL databases.
* Docker initialization creating all required databases.
* Default PostgreSQL connection settings for local development.
* Future vector search implemented through the PostgreSQL pgvector extension.