# Decision 1: Response Envelope Deferred

## Reason
- Current flask-openapi3 integration requires updating
  a large number of response schemas.
- Swagger documentation is already partially inconsistent:
  - custom validation bypasses OpenAPI validation
  - nested blueprints are not fully represented
  - interactive testing is limited
- Cost outweighs benefit at current project stage.

## Future
- Revisit after Redis/Celery/AI infrastructure is complete.
- Consider replacing flask-openapi3 entirely if maintenance burden grows.

# Decision 2: Environment-Based Configuration with Pydantic Settings + Override Layer Pattern

## Decision

Use a single BaseSettings model (Pydantic) as the source of truth for configuration,
and apply environment-specific overrides via explicit override functions rather than
inheritance-based settings classes.

Final structure:
- BaseAppSettings → defines all configuration fields and loads from .env/system env
- Override functions → return environment-specific overrides (dict)
- get_settings() → composes final configuration using base + overrides

## Reason

- Pydantic Settings already supports environment variable loading, making inheritance-based
  overrides (TestingSettings / ProductionSettings) redundant and error-prone.
- Class-based overrides were unintentionally unreliable due to environment variables
  taking precedence over Python class defaults.
- Inheritance-based configuration introduced hidden behavior and made it unclear which
  values are actually active at runtime.
- A composition-based override system makes configuration:
  - more explicit
  - easier to debug
  - easier to test
  - more aligned with production deployment practices (CI/CD, Docker, Kubernetes)
- Avoids duplication of environment-specific settings logic across multiple classes.

## Tradeoffs

- Slightly more boilerplate compared to subclass-based settings.
- Requires explicit override functions instead of implicit class inheritance.
- Developers must understand override precedence (base → overrides → final settings).

## Benefits

- Clear configuration flow: .env → BaseSettings → overrides → final settings
- No hidden precedence bugs between .env and subclass defaults
- Easier testing with isolated override functions
- Scales cleanly as more environments or features are added
- Works naturally with CI/CD environments where env vars are injected externally

## Future Considerations

- May evolve into a structured configuration system with:
  - feature flags
  - secret management (Vault / cloud secrets manager)
  - environment-specific config modules (dev/staging/prod/testing)
- If configuration complexity grows significantly, consider adopting a dedicated config
  management layer or service-style config loader.

# Decision 3: Migrated from google-generativeai to google-genai

## Reason:
- Google has depricated old `google-generativeai` package
- The package is no longer is recieving updates or bug fixes
- All support for the `google.generativeai` package has ended
- Every user has shifted to `google.genai`

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

# Decision 5: Deferred Full Session Management

## Decision

Do not implement full session management during Phase 3.

The current authentication system will use:

- Short-lived JWT access tokens
- Rotating refresh tokens stored in the database
- Refresh token revocation on logout
- Refresh token expiration checks
- UUID-based token records

Advanced session management will be postponed to a future improvement phase.

## Reason

The primary goal of this project is to learn and implement production-grade backend and AI engineering concepts rather than build a publicly deployed authentication platform.

The current refresh-token architecture already provides:

- Stateless access tokens
- Secure refresh token rotation
- Logout support
- Token revocation
- Expiration handling

This is sufficient for the project's current requirements and learning objectives.

Implementing full session management would introduce significant additional complexity:

- Device tracking
- Session metadata
- Session dashboards
- Multi-device logout
- Last activity tracking
- Session expiration policies
- Redis integration for session caching

These features are valuable for large-scale production systems but are not required for the current scope.

## Current Authentication Architecture

Access Token:
- JWT
- Short-lived
- Stored client-side

Refresh Token:
- Random opaque token
- SHA256 hash stored in database
- Rotated on refresh
- Deleted on logout
- Expiration enforced

## Deferred Features

The following items are intentionally postponed:

### Session Table

Possible future structure:

- session_id
- user_id
- refresh_token_hash
- device_name
- ip_address
- user_agent
- created_at
- last_used_at
- expires_at
- revoked_at

### User Session Management

- View active sessions
- Logout specific devices
- Logout all devices
- Session activity history

### Redis Enhancements

- JWT blacklist cache
- Session cache
- Automatic expiration cleanup

### Security Enhancements

- Device fingerprinting
- Suspicious login detection
- Concurrent session limits

## Tradeoffs

### Benefits

- Simpler codebase
- Faster development
- Lower maintenance burden
- Focus remains on AI infrastructure and backend architecture
- Authentication remains secure enough for project goals

### Costs

- No device-level session visibility
- No multi-device management
- No session activity tracking
- Some enterprise-grade features unavailable

## Future Revisit Criteria

Re-evaluate full session management if:

- The application becomes publicly deployed
- Multiple devices per user become common
- Administrative user management is required
- Security requirements increase significantly
- Redis infrastructure is already introduced for other features

Until then, rotating refresh tokens with revocation provide sufficient authentication guarantees for the project.

# Decision 6: Deferred Access Token Blacklisting

## Decision

Do not implement access-token blacklisting during Phase 3.

## Reason

The current authentication architecture uses:

- Short-lived access tokens (15 minutes)
- Refresh token rotation
- Refresh token revocation on logout

When a user logs out, the refresh token is revoked immediately, preventing issuance of new access tokens. The remaining risk window is limited to the lifetime of the current access token (15 minutes), which is acceptable for the project's scope.

Implementing access-token blacklisting would introduce:

- Redis dependency
- JWT `jti` tracking
- Additional authentication checks on every protected request

without providing significant practical benefit for a learning-focused, non-public project.

## Future Revisit Criteria

Consider access-token blacklisting if:

- Access token lifetime increases significantly
- The application becomes publicly deployed
- Security requirements become stricter
- "Logout everywhere" functionality is introduced