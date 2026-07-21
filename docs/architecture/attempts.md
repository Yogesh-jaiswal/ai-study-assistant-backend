# Attempt Architecture

## Overview

The Attempt layer is responsible for evaluating user submissions against previously generated AI content.

Unlike AI generation, attempt evaluation is not always AI-powered. Some content types, such as quizzes, can be evaluated deterministically, while others, such as descriptive exams, require AI-assisted evaluation.

The attempt infrastructure provides a unified evaluation pipeline regardless of how the evaluation is performed.

```
Route
    ↓
Attempt Service
    ↓
Attempt Context
    ↓
Attempt Validator
    ↓
Celery Task
    ↓
Attempt Loader
    ↓
Evaluation Bundle
    ↓
Attempt Job
    ↓
Feature Evaluator
    ↓
(Optional AI Engine)
    ↓
Persist Attempt
```

---

# Design Goals

The attempt infrastructure was designed around the following principles.

- Support both AI-based and deterministic evaluation.
- Keep evaluation independent from HTTP handling.
- Preserve the original AI content.
- Allow multiple attempts for the same AI content.
- Keep evaluation workflows feature-specific.
- Reuse the same asynchronous infrastructure as AI generation.

---

# Architecture

## Attempt Context

Every evaluation request first creates an `AttemptContext`.

The AttemptContext contains:

- AI Content identifier
- User submitted answers

The context contains identifiers and user input only.

It intentionally avoids loading database resources.

---

## Validation

Before evaluation begins, the AttemptValidator verifies:

- AI Content existence
- Notebook ownership
- Content compatibility
- Submitted answer validity

Only valid attempts proceed to evaluation.

---

## Attempt Loader

The Attempt Loader is responsible for retrieving the resources required for evaluation.

It converts the AttemptContext into an EvaluationBundle.

The loader currently retrieves:

- Generated AI content
- Submitted answers

Additional resources may be added in the future without modifying evaluators.

---

## Evaluation Bundle

The EvaluationBundle is the common contract between infrastructure and feature evaluators.

It contains prompt-ready evaluation resources rather than ORM models.

Typical contents include:

- Generated AI content
- Submitted answers

Feature evaluators remain completely unaware of how these resources were stored or retrieved.

---

## Attempt Jobs

Attempt Jobs coordinate feature-specific evaluation workflows.

Responsibilities include:

- Invoking the correct evaluator
- Performing feature-specific post-processing
- Merging evaluation results when required
- Returning normalized evaluation metadata

Each AI content type owns its own Attempt Job.

Examples include:

- Quiz Attempt Job
- Exam Attempt Job

---

## Feature Evaluators

Each feature owns its own evaluator.

Responsibilities include:

- Evaluating submitted answers
- Producing feature-specific evaluation
- Returning normalized results

Evaluators remain independent from persistence and HTTP handling.

### Deterministic Evaluation

Some evaluators require no AI.

Example:

```
Quiz Evaluator

Question
    ↓
Compare Answer
    ↓
Score
```

### AI-assisted Evaluation

Some evaluators require AI reasoning.

Example:

```
Prompt
    ↓
AI Engine
    ↓
Evaluation
```

Both evaluators expose the same interface to the Attempt Job.

---

## Feature-specific Post-processing

Some evaluation workflows require additional processing after evaluation.

For example:

- Quiz evaluation directly produces the final evaluation.
- Exam evaluation merges AI feedback back into the original question paper before persistence.

This logic belongs to the Attempt Job rather than the evaluator or AI Engine.

---

## Persistence

Each completed evaluation creates a UserAttempt.

A UserAttempt stores:

- Evaluation status
- Total marks
- Obtained marks
- Percentage
- Evaluation payload

Multiple attempts may exist for the same AI Content.

The original generated content is never modified.

---

# Extensibility

The architecture is designed to support additional evaluation strategies.

Examples include:

- Flashcard self-assessment
- Coding evaluation
- Interactive simulations
- Peer review
- Hybrid AI and rule-based evaluation

Most new evaluation types only require:

- New evaluator
- New Attempt Job

The infrastructure remains unchanged.

---

# Design Principles

## Preserve Generated Content

Generated AI content is immutable.

All evaluation results are stored separately.

---

## Feature-owned Evaluation

Each feature owns:

- Evaluator
- Evaluation schema
- Attempt Job

Infrastructure remains feature-agnostic.

---

## Unified Pipeline

Whether evaluation is deterministic or AI-assisted, every feature follows the same orchestration pipeline.

This allows the surrounding infrastructure to remain completely generic.

---

# Future Improvements

Potential future improvements include:

- Partial attempt saving
- Timed attempts
- Attempt analytics
- Rubric-based grading
- Plagiarism detection
- Retryable evaluation
- Manual re-evaluation
- Evaluation versioning

---

# Guiding Principle

The attempt infrastructure coordinates evaluation.

Feature evaluators decide **how** evaluation happens.

Attempt Jobs decide **how evaluation is assembled**.

Infrastructure decides **how evaluation is executed and persisted**.

This separation allows new evaluation strategies to be introduced without modifying the underlying attempt infrastructure.