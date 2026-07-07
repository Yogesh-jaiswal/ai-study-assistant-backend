# Decision 4: UUID Migration with Boundary Validation Pattern

## Decision

Migrate all primary keys and foreign keys from integer identifiers to UUIDs.

Use UUID validation at API boundaries while preserving string identifiers internally throughout services and repositories.

Pattern:

* Database stores UUID values as strings
* Pydantic schemas validate UUID format
* Route parameters are validated as UUIDs
* JWT subject claims are normalized through UUID validation
* Services and repositories continue using string identifiers

## Reason

A full UUID-object migration across all application layers would require extensive type conversion and repository changes while providing limited additional value.

The primary goals of the migration were:

* eliminate sequential identifier enumeration
* prevent accidental ID mixups across resources
* improve security through non-predictable identifiers
* improve test reliability

Boundary validation achieves these goals without introducing UUID conversion complexity throughout the codebase.

## Tradeoffs

Pros:

* Strong request validation
* UUID format enforcement
* Simpler service layer
* Minimal repository changes
* Reduced migration risk

Cons:

* Internal typing uses strings instead of UUID objects
* UUID validation is concentrated at application boundaries rather than every layer

## Examples

Request validation:

```python
class NotebookIDPathParams(BaseModel):
    notebook_id: UUID
```

JWT validation:

```python
g.user_id = str(UUID(user_id))
```

Service layer:

```python
def get_notebook(notebook_id: str, user_id: str):
    ...
```

## Outcome

UUID migration completed successfully with all integration tests passing.

The application now rejects invalid UUIDs before reaching business logic while preserving a simple internal identifier representation.