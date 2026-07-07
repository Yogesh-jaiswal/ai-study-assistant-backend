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