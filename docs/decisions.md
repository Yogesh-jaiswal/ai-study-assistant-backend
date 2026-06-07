# Decision 1: Response Envelope Deferred

Reason:
- Current flask-openapi3 integration requires updating
  a large number of response schemas.
- Swagger documentation is already partially inconsistent:
  - custom validation bypasses OpenAPI validation
  - nested blueprints are not fully represented
  - interactive testing is limited
- Cost outweighs benefit at current project stage.

Future:
- Revisit after Redis/Celery/AI infrastructure is complete.
- Consider replacing flask-openapi3 entirely if maintenance burden grows.