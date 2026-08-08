# RAG Evaluation

## Overview

The RAG Evaluation module provides an automated way to measure the quality of the Retrieval-Augmented Generation (RAG) pipeline used by the AI Study Assistant backend.

Unlike unit tests that verify correctness of individual components, the evaluation pipeline measures the quality of the complete retrieval workflow:

```
Question
      ↓
Similarity Search
      ↓
Retrieved Chunks
      ↓
Context Assembly
      ↓
LLM Generation
      ↓
DeepEval Metrics
      ↓
Evaluation Report
```

The generated report helps identify retrieval failures, hallucinations, and answer quality issues while tracking improvements as the retrieval pipeline evolves.

---

# Purpose

The evaluation module exists to answer questions such as:

* Is the retriever finding relevant information?
* Does the generated answer stay grounded in retrieved context?
* Is the generated answer relevant to the user's question?
* Does retrieval quality improve after changing chunking, embeddings, or ranking?

The module is intended for offline evaluation and development rather than production request handling.

---

# Architecture

The evaluation pipeline consists of several independent components.

```
rag_evaluation/
│
├── dataset.json
├── corpus.md
├── state.json
├── report.json
├── evaluate.py
├── setup.py
└── deepeval_judge.py
```

---

## setup.py

Creates a temporary evaluation environment.

Responsibilities include:

* creating evaluation resources
* importing the evaluation corpus
* uploading the corpus
* generating document chunks
* generating embeddings
* persisting evaluation state
* preparing the retrieval database

The setup step ensures every evaluation starts from a predictable state.

---

## dataset.json

Contains evaluation samples.

Each entry defines:

* question
* expected output

Example:

```json
{
    "question": "What is Retrieval-Augmented Generation?",
    "expected_output": "Retrieval-Augmented Generation combines retrieval with language generation."
}
```

The dataset intentionally remains small during development to minimize API usage.

---

## corpus.md

The evaluation corpus contains the reference knowledge used during benchmarking.

Unlike the evaluation dataset, which defines questions and expected answers, the corpus provides the documents that are indexed into the vector database before evaluation begins.

During setup:

- the corpus is imported,
- chunked,
- embedded,
- stored in the vector database.

This guarantees that every evaluation executes against the same knowledge base, making benchmark results reproducible.

---

## state.json

The setup phase creates temporary application resources required for evaluation.

These include identifiers such as:

- evaluation user
- evaluation notebook
- uploaded document

The generated identifiers are persisted in `state.json` so the evaluation runner can access them without recreating resources during the same execution.

This file is considered an internal implementation detail and is regenerated automatically by the setup process.

---

## evaluate.py

The evaluation runner coordinates the complete workflow.

For every dataset entry it performs:

1. similarity search
2. context assembly
3. answer generation
4. metric evaluation
5. report generation

This module serves as the primary entry point.

---

## deepeval_judge.py

DeepEval requires an LLM to act as the evaluation judge.

The project provides a custom Gemini-based judge implementation that satisfies DeepEval's expected interface while remaining completely independent from the application's AI infrastructure.

The evaluation judge intentionally bypasses the backend AI layer because DeepEval requires a different interaction model than the application's business-oriented AI services.

This separation keeps the evaluation pipeline isolated from future changes to the production AI architecture.

---

## report.json

The generated report contains:

* evaluation summary
* individual metric results
* execution durations
* failure reasons

Example:

```text
Summary
│
├── Generated Time
├── Question Count
└── Metric Summary

Results
│
└── Question
      ├── Metric
      ├── Score
      ├── Pass
      ├── Duration
      └── Reason
```

Reports are overwritten on every execution.

---

# Evaluation Metrics

The current evaluation pipeline measures three aspects of RAG quality.

| Metric               | Purpose                                                                                 |
| -------------------- | --------------------------------------------------------------------------------------- |
| Answer Relevancy     | Measures whether the generated answer addresses the user question                       |
| Faithfulness         | Detects hallucinations by checking whether the answer is supported by retrieved context |
| Contextual Relevancy | Measures whether retrieved chunks are relevant to the query                             |

These metrics represent the commonly used **RAG Triad** for evaluating retrieval systems.

---

# Running the Evaluation

Run the evaluation pipeline using the following steps.

1. Start the required Docker services.

```bash
docker compose -f docker/compose.yaml up -d
```

2. Run the evaluation.

```bash
python -m rag_evaluation.evaluate
```

3. Stop the Docker services.

Remove containers and volumes:

```bash
docker compose -f docker/compose.yaml down -v
```

Or keep the database and Redis volumes:

```bash
docker compose -f docker/compose.yaml down
```

The command performs:

* environment setup
* dataset loading
* retrieval
* answer generation
* metric evaluation
* report generation

---

# Evaluation Environment

The evaluation environment differs slightly from the normal development configuration.

Current overrides include:

* Celery eager execution
* Celery eager exception propagation
* Warning log level

These overrides allow the evaluation pipeline to:

* execute asynchronous tasks synchronously,
* surface task failures immediately,
* reduce logging noise generated by external libraries during benchmark execution.

---

# Current Limitations

The evaluation pipeline currently has several practical limitations.

### Gemini Free Tier

DeepEval metrics internally perform multiple LLM calls.

Even a single evaluation question may require several model invocations.

As a result, free-tier Gemini rate limits are frequently reached before every metric completes.

Current behavior:

* Successful metrics are preserved.
* Failed metrics are written to the report.
* Remaining metrics are skipped after quota exhaustion.
* The evaluation process never aborts because of API quota failures.

### Small Evaluation Dataset

Only a very small evaluation dataset is currently maintained to minimize API usage during development.

Larger datasets will be introduced when a more suitable evaluation model becomes available.

---

# Design Decisions

Several architectural decisions affect this module.

* Evaluation uses the project's own AI infrastructure instead of DeepEval's default providers.
* Reports are generated even if some metrics fail.
* Retrieval evaluation is deterministic because setup recreates the evaluation state every run.
* API quota failures are treated as evaluation failures rather than application failures.

Additional rationale is documented in the Architecture Decision Records (ADRs).

---

# Future Improvements

Planned improvements include:

* Automated evaluation dataset generation
* Larger benchmark datasets
* Context Precision metric
* Context Recall metric
* Multiple evaluation scenarios
* CI integration
* Historical report comparison
* Local judge model support
* Automatic environment configuration

---

# Directory Structure

```
rag_evaluation/
│
├── dataset.json
├── report.json
├── deepeval_judge.py
├── evaluate.py
├── setup.py
└── README.md
```

---

# References

* DeepEval RAG Evaluation documentation
* DeepEval Metrics documentation
* RAG Triad guide
