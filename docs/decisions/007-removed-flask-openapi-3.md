# Decision 7: Remove Flask-OpenAPI3 and Use Native Flask Routing

## Decision

Remove Flask-OpenAPI3 from the project and migrate fully to native Flask.

Changes:

* Replace `OpenAPI` with `Flask`
* Replace `APIBlueprint` with `Blueprint`
* Remove OpenAPI route metadata
* Remove OpenAPI response declarations
* Remove OpenAPI path parameter schemas
* Use native Flask route parameters directly
* Keep Pydantic for request validation and response serialization

Example:

Before:

```python
@summary_bp.delete(
    "/<string:summary_id>",
    summary="Delete summary",
    responses={...}
)
def delete_summary(path: SummaryIDPathParams):
```

After:

```python
@summary_bp.delete("/<uuid:summary_id>")
def delete_summary(summary_id: UUID):
```

## Reason

Flask-OpenAPI3 introduced significant boilerplate while providing limited value at the current stage of the project.

Issues encountered:

* Route definitions became verbose
* Response schemas required constant maintenance
* Swagger documentation was partially inaccurate
* Nested blueprint behavior was not fully represented
* Validation was already handled through custom logic and Pydantic models
* OpenAPI integration increased coupling to a specific framework

The project currently has no external consumers and does not require generated API documentation.

## Benefits

* Simpler route definitions
* Less framework-specific code
* Easier maintenance
* Faster feature development
* Reduced boilerplate
* Easier future framework migration

## Tradeoffs

* Loss of automatic Swagger/OpenAPI generation
* Manual API documentation may be required later
* API contracts are no longer generated automatically

## Future Considerations

If the API becomes publicly consumed:

* Reintroduce OpenAPI generation
* Evaluate FastAPI
* Evaluate dedicated API documentation tooling

Until then, development speed and maintainability take priority.