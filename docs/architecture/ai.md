# AI Architecture

## Overview

The AI layer provides a reusable infrastructure for all AI-powered features in the backend. Its purpose is to isolate provider-specific logic from business logic while allowing new AI features to be implemented with minimal changes to the underlying infrastructure.

The architecture follows the same layered philosophy as the rest of the backend:

```
Feature
    ↓
Generator
    ↓
Prompt
    ↓
AI Engine
    ↓
AI Provider
    ↓
Validated Response
```

Business features never communicate directly with AI providers. Instead, every request passes through the AI Engine, which selects the configured provider and returns a validated response.

---

## Design Goals

The AI infrastructure was designed around the following principles:

* AI providers must be replaceable without modifying business features.
* Business features should own their own prompts and response schemas.
* The AI Engine should remain completely independent of business logic.
* Adding a new AI feature should not require modifying the AI Engine.
* AI responses should always be validated before entering the business layer.
* Provider-specific implementation details should remain isolated.

---

## Architecture

### Feature Layer

Each AI feature is responsible for defining:

* Prompt construction
* Response schema
* Generator

Example:

```
services/
    summaries/
        generator.py
        summary_prompt.py
        response_schema.py
```

The feature owns everything specific to its business logic.

---

### Generator

The generator coordinates a single AI feature.

Responsibilities:

* Build the prompt
* Pass the prompt and response schema to the AI Engine
* Return the validated result

The generator contains no provider-specific code.

---

### Prompt

Every feature owns its own prompt.

Examples:

```
summary_prompt.py
chat_prompt.py
quiz_prompt.py
exam_prompt.py
```

There is intentionally no global prompt builder because prompts are considered business logic rather than infrastructure.

---

### Response Schema

Each feature defines its own Pydantic response schema.

Example:

```
SummaryResponse
ChatResponse
QuizResponse
```

Response schemas serve multiple purposes:

* Validate AI output
* Document expected structure
* Provide provider-independent contracts
* Support provider-native structured generation

These schemas are intentionally separate from API response schemas because they represent AI contracts rather than HTTP responses.

---

### AI Engine

The AI Engine is the central entry point for all AI requests.

Responsibilities:

* Select the configured provider
* Forward prompt and response schema
* Return the provider result

The engine knows nothing about:

* Summaries
* Chat
* Flashcards
* Exams
* Mind maps
* Business logic

Its only inputs are:

* Prompt
* Response schema

This separation allows new AI features to be added without modifying the engine.

---

### Providers

Providers implement communication with individual AI models.

Current providers:

* Gemini
* Fake Provider

Future providers may include:

* OpenAI
* Claude
* Ollama
* LM Studio

Providers are registered inside the engine and remain completely independent of business features.

-> Current registration is static. A provider registration system may be introduced during a future architecture refactor.

---

## Fake Provider

The Fake Provider exists to support testing and local development.

Instead of manually maintaining fake responses for every feature, it automatically generates valid responses directly from the supplied Pydantic response schema.

Benefits:

* No duplicated fake response definitions
* Automatic support for new AI features
* Reduced maintenance
* Consistent response validation

---

## Legacy AI Architecture

The project originally used a single shared AI client together with a global prompt builder.

This implementation remains under the legacy package to preserve compatibility with earlier routes while the new architecture replaces it incrementally.

The legacy implementation is intentionally isolated and no new features should depend on it.

---

## Future Improvements

Potential improvements include:

* Dynamic provider registration
* Request retry policies
* Response caching
* Token accounting
* Usage monitoring
* Cost tracking

These improvements belong to the infrastructure layer and should not affect business features.

---

## Extensibility

The current architecture is expected to support most future AI features such as:

* Summaries
* Chat
* Flashcards
* Quizzes
* Exams
* Mind Maps

More complex workflows may build additional layers on top of this architecture.

For example:

```
Prompt
    ↓
AI Engine
    ↓
Structured Content
    ↓
Slide Generator
```

or

```
Prompt
    ↓
AI Engine
    ↓
Podcast Script
    ↓
Speech Generation Pipeline
```

These workflows extend the AI infrastructure rather than replacing it.

---

## Guiding Principle

The AI infrastructure should remain generic.

Business logic belongs to individual AI features.

Providers belong to the infrastructure.

Neither layer should know about the other beyond the prompt and response schema contract.