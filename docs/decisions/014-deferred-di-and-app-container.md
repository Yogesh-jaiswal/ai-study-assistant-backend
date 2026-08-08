# Decision 014: Deferred Dependency Injection and Application Container

## Decision

Do not introduce a dependency injection container or application composition root during the current architecture.

The backend will continue using configuration-driven dependency selection through application settings rather than runtime dependency injection.

The previously proposed application container, provider registries, and composition root have been deferred until a future architectural need justifies their complexity.

---

## Reason

The project originally planned to introduce a dependency injection container to support:

- Runtime provider swapping
- Multiple embedding implementations
- Multiple AI providers
- Test-specific service implementations

As the backend architecture matured, these requirements became significantly less important.

Current observations include:

- AI provider selection is already abstracted behind the AI Engine.
- Only one embedding implementation is used during normal application execution.
- Runtime implementation swapping is not required in production.
- Infrastructure changes naturally require application restart.
- Most testing scenarios execute under a single application configuration.

Introducing a dependency injection container would add an additional architectural layer without solving an existing problem.

---

## Current Behavior

The backend currently uses configuration-driven dependency selection.

Application settings determine:

- AI provider
- Embedding provider
- Database configuration
- Celery execution mode
- Environment-specific behavior

Changing an implementation simply requires updating configuration and restarting the application.

This matches the expected deployment workflow for production systems.

---

## Why Dependency Injection Was Deferred

Several practical observations led to this decision.

### Runtime provider swapping is unnecessary

The backend never needs to switch between providers while the application is running.

Deployment-time configuration is sufficient.

### Existing abstractions already isolate business logic

The backend already separates business logic from infrastructure through dedicated service layers.

Examples include:

```
Feature
    ↓
Generator
    ↓
AI Engine
    ↓
Configured Provider
```

Business features remain independent from provider implementations without requiring a dependency injection container.

### Celery limits configuration switching

Celery workers load configuration once during startup.

Even with dependency injection, changing providers or execution profiles during a test session would still require restarting the worker.

Therefore, dependency injection would not solve the current testing limitations.

### Additional complexity

Introducing:

- Application container
- Composition root
- Provider factories
- Service registries

would increase the architectural complexity while providing little practical benefit for the current project scope.

---

## Future Revisit Criteria

Dependency injection should be reconsidered if future requirements introduce:

- Runtime plugin loading
- Multi-tenant provider selection
- Multiple embedding providers running simultaneously
- Dynamic provider registration
- Third-party extension ecosystem
- Runtime feature modules
- Complex object graph construction

If these requirements emerge, introducing an application container will become justified.

---

## Implementation Notes

The previous experimental implementation included:

```
Application Container
Composition Root
Provider Registries
Provider Factories
```

This implementation has been intentionally removed from the active architecture.

The current project instead follows a configuration-driven architecture where application settings determine which concrete implementations are used.

This keeps the backend simpler while remaining extensible through future configuration changes.

---

## Consequences

### Advantages

- Simpler architecture
- Fewer abstraction layers
- Easier debugging
- Lower maintenance cost
- Explicit service construction
- Configuration remains the single source of truth

### Trade-offs

- Runtime dependency swapping is not supported.
- Infrastructure changes require application restart.
- Future plugin-based architectures may require reintroducing an application container.

At the current project scale, these trade-offs are considered acceptable.