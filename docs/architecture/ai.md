# AI Infrastructure

## Overview

The AI layer provides a reusable infrastructure for all AI-powered features in the backend. Its purpose is to isolate provider-specific logic from business logic while allowing new AI features to be implemented with minimal changes to the underlying infrastructure.

The infrastructure follows the same layered philosophy as the rest of the backend:

```
Route
    ↓
Generation Service
    ↓
Generation Context
    ↓
Generation Validator
    ↓
Celery Task
    ↓
Bundle Loader
    ↓
GenerationBundle
    ↓
Generation Job
    ↓
Generator
    ↓
Prompt
    ↓
AI Engine
    ↓
Provider
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
        summar_generator.py
        summary_prompt.py
        summary_schema.py
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

### Generation Jobs

Generation Jobs act as orchestration adapters between Celery tasks and individual AI feature generators.

Responsibilities:

* Receive generation context
* Receive job options
* Convert GenerationBundle into prompt-ready context
* Invoke the correct feature generator
* Pass provider-specific testing options to the AI Engine when required
* Return normalized AI content

Generation Jobs act as the execution boundary between Celery and individual AI features. They encapsulate feature-specific generation options while keeping Celery unaware of business logic.

---

### Feature-specific Post-processing

Some AI features require post-processing after generation.

For example, exam generation merges AI-generated question content into a predefined blueprint before persistence.

This post-processing remains inside the feature's AI Job rather than the AI Engine, ensuring infrastructure remains independent of business logic.

---

### Generation Context

Every AI generation request first creates a `GenerationContext`.

The GenerationContext contains identifiers for every resource required during generation rather than the resources themselves.

Current supported resources include:

* Notes
* Reference papers
* Exam blueprints

Additional resource types can be introduced without changing feature generators.

The GenerationContext travels through the asynchronous pipeline until it reaches the Celery worker.

---

### Resource Validation

Before loading any resources, the Celery worker validates the GenerationContext.

Validation includes:

* Resource existence
* Ownership and access control
* Processing status
* Resource type compatibility

Only validated resources proceed to the loading stage.

---

### Resource Assembly

After validation, resources are loaded and converted into a provider-independent `GenerationBundle`.

The GenerationBundle contains prompt-ready resources rather than database models.

Current resource types include:

* Notes
* Reference papers
* Exam blueprints

Generators remain completely unaware of how resources are stored or retrieved and only consume the GenerationBundle.

This separation allows additional resource types to be introduced without modifying generators.

---

### Prompt

Prompts receive a normalized `GenerationBundle` rather than individual resources.

Example:

```
Resources:

Notes:
...

---

References:
...
```

Then each feature uses this context build its own prompt.

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

```text
SummaryResponse
QuizResponse
FlashcardResponse
MindMapResponse
ExamResponse
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

Its inputs are:

* Prompt
* Response schema
* Job options

The AI Engine treats job options as opaque metadata and forwards them directly to the selected provider without interpreting them.

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

Providers may optionally consume provider-specific job options. Unknown options should be ignored, allowing feature-specific testing behavior without affecting production providers.

AI model registration is config driven. To change the model requires change in configurations and server restart.

---

## Fake Provider

The Fake Provider exists to support testing and local development.

Instead of manually maintaining fake responses for every feature, it automatically generates valid responses directly from the supplied Pydantic response schema.

For features requiring deterministic test behavior (such as generating a fixed number of quiz questions), optional provider-specific job options may be supplied. These options are ignored by production providers but allow the Fake Provider to generate predictable test data without introducing feature-specific logic into the AI Engine.

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

The current architecture is designed to support independent AI features while allowing each feature to introduce its own prompts, response schemas, post-processing, and resource requirements without modifying shared infrastructure.

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

Business features own:

* Prompts
* Response schemas
* Generation Jobs
* Post-processing logic

The infrastructure owns:

* Resource validation
* Resource loading
* AI Engine
* Providers

The only contract between both layers is:

* GenerationBundle
* Prompt
* Response schema
* Job options

This separation allows new AI capabilities to be introduced without modifying the underlying AI infrastructure.