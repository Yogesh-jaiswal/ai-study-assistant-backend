# Database Architecture

## Overview

The database layer is responsible for persisting all application data while remaining completely independent from business logic.

The project uses PostgreSQL together with SQLAlchemy ORM and follows a relational-first design. Relationships between entities are represented explicitly through foreign keys and relationship tables rather than embedding relational data inside JSON.

The database is designed to support the application's current feature set while remaining flexible enough to accommodate future AI capabilities without requiring large schema migrations.

---

## Design Goals

The database architecture follows these principles:

* Normalize business entities.
* Store relationships explicitly.
* Preserve referential integrity.
* Keep persistence independent from business logic.
* Avoid feature-specific database duplication.
* Support future AI features through extensible schemas.

---

# Layer Position

```
Routes
    ↓
Services
    ↓
Repositories
    ↓
Database
```

Only repositories communicate directly with the database.

Business logic never performs SQL operations directly.

---

# Core Entities

The backend currently revolves around several primary entities.

```
User
    │
    ├── Notebook
    │       │
    │       ├── Upload
    │       │       │
    │       │       ├── Chunks
    │       │       └── Embeddings
    │       │
    │       └── AI Content
    │               │
    │               └── User Attempt
    │
    └── Exam Blueprints
```

Each entity owns a single responsibility.

Examples:

* Users own notebooks and exam blueprints.
* Notebooks organize uploaded study material.
* Uploads represent original learning resources.
* Chunks and embeddings support retrieval.
* AI Content stores generated learning material.
* User Attempts store evaluations for generated AI content.

---

# Relationship Philosophy

Relationships are represented explicitly using foreign keys.

Examples include:

```
Notebook
    ↓
Upload

Notebook
    ↓
AI Content
```

Many-to-many relationships are modeled using dedicated relationship tables.

Example:

```
Upload
    ↓
UploadAIContentRelationship
    ↑
AI Content
```

This allows:

* One upload to contribute to multiple generated contents.
* One generated content to reference multiple uploads.

The database therefore models provenance explicitly instead of duplicating generated content.

---

# AI Content Storage

All generated AI features share a single generic table.

```
AI Content

id
notebook_id
title
content_type
content
upload_count
generated_at
```

Evaluation results are stored separately inside the UserAttempt table.

Each attempt references a single AI Content record while storing:

* evaluation metadata
* evaluation status
* obtained marks
* evaluation payload

This separation allows multiple attempts to exist for the same generated content without modifying the original AI content.

Examples include:
Examples of JSON data:

* summary
* quiz questions
* flashcards
* mind maps
* exam blueprints
* AI evaluation payloads

Using a shared table avoids creating a separate database table for every AI feature while allowing new content types to be introduced with minimal schema changes.

Only the generated payload is stored as JSON.

Relationships and ownership remain relational.

---

# JSON Usage

JSON columns are intentionally limited to AI-generated content and Exam Blueprints.

Business entities are never represented using JSON.

Examples of relational data:

* notebook_id
* upload_id
* user_id
* ownership
* relationships

Examples of JSON data:

* summary
* quiz questions
* flashcards
* mind maps
* exam blueprints

This keeps relational queries efficient while allowing AI payloads to evolve independently.

---

# Repository Pattern

All persistence is isolated behind repositories.

Repositories are responsible for:

* CRUD operations
* Query construction
* Persistence
* Transaction management

Repositories do not contain business logic.

Services coordinate workflows while repositories only manage persistence.

---

# Ownership Enforcement

Ownership is verified through repository queries rather than separate authorization checks.

Typical pattern:

```
Requested Resource
    ↓
Parent Notebook
    ↓
Owner (User)
```

Queries join parent entities to ensure users may only access resources they own.

This prevents accidentally exposing resources through direct identifier lookups.

---

# Cascading Deletes

Relationships use cascading deletes to maintain referential integrity.

Examples include:

* Notebook deletion removes uploads.
* Upload deletion removes chunks.
* Upload deletion removes embeddings.
* AI Content deletion removes relationship records.
* AI Content deletion removes user attempts.

This prevents orphaned records while simplifying cleanup logic.

---

# Transaction Philosophy

Each repository operation is treated as a single transaction.

Successful operations commit once.

Failures roll back the entire transaction.

This ensures database consistency even when multiple related objects are created simultaneously.

Examples include:

* AI content creation together with relationship records.
* File processing together with chunks and embeddings.
* Attempt evaluation together with evaluation metadata.

---

# Retrieval Support

The retrieval pipeline stores processed document information separately from generated AI content.

Current retrieval storage includes:

* Uploaded document text
* Processed chunks
* Vector embeddings

Generated AI content is intentionally not used as retrieval input.

This separation allows retrieval architecture to evolve independently.

---

# Extensibility

The schema is designed so that new AI features rarely require structural database changes.

Most future features can reuse:

* AI Content
* User Attempts
* Upload relationships
* Existing ownership model

Future additions are expected to extend metadata and retrieval capabilities rather than introducing new top-level entities.

---

# Future Improvements

Potential future improvements include:

* Rich retrieval metadata
* Source citation metadata
* Document hierarchy metadata
* Retrieval evaluation datasets
* Soft deletes
* Audit history
* Full-text search indexes
* Multi-notebook retrieval support

These additions should extend the current schema rather than replace it.

---

# Guiding Principle

The database stores facts.

Business rules belong in services.

Queries belong in repositories.

Relationships remain relational.

Only AI-generated payloads, exam blueprints and evaluation payloads are stored as JSON.