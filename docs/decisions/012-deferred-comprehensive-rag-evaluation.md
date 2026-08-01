# Decision 012: Deferred Comprehensive RAG Evaluation

## Decision

Complete the RAG evaluation infrastructure during Phase 4 while deferring comprehensive benchmark execution until sufficient Gemini API quota is available.

The evaluation pipeline, reporting infrastructure, and DeepEval integration are considered production-ready even though full benchmark execution cannot currently be completed under the Gemini API Free Tier limits.

## Reason

The project uses DeepEval together with Gemini as the evaluation judge model.

Unlike application inference, DeepEval performs multiple LLM calls internally for every evaluation metric. A single test case may require several judge requests for:

* Answer Relevancy
* Faithfulness
* Contextual Relevancy

This causes the evaluation process to consume Gemini API requests much faster than normal application usage.

The current implementation successfully executes evaluation until external Gemini API quotas are exhausted. The resulting report still preserves all completed metric results while gracefully recording failures caused by external quota limits.

Because this limitation originates from the external evaluation provider rather than the retrieval pipeline itself, extending Phase 4 would not improve the implementation.

## Current Behavior

The evaluation pipeline currently provides:

* Dataset loading
* Automatic environment setup
* Retrieval execution
* Answer generation
* DeepEval metric execution
* JSON report generation
* Partial report preservation on external API failures
* Graceful handling of Gemini quota exhaustion

When Gemini returns a `429 RESOURCE_EXHAUSTED` error:

* Completed metrics remain in the report.
* Failed metrics are recorded with the provider error.
* Remaining metrics are skipped when further evaluation is impossible.
* The evaluation process still produces a valid report instead of terminating unexpectedly.

## Known Limitation

The current benchmark is constrained by Gemini Free Tier quotas.

Even with delays between metric executions, DeepEval may exceed the available Requests Per Minute (RPM) or Requests Per Day (RPD) limits because each metric performs multiple internal judge requests. Gemini enforces both RPM and RPD quotas, and exceeding either returns a `429 RESOURCE_EXHAUSTED` error.

This limitation does not affect:

* Retrieval quality
* Context assembly
* Chat generation
* Report generation

It only affects the number of evaluation metrics that can be completed during a single benchmark run.

## Future Revisit Criteria

Comprehensive evaluation should be revisited when one or more of the following becomes available:

* A paid Gemini API tier
* Higher Gemini API quotas
* An alternative evaluation judge model
* A locally hosted evaluation model
* Batched or distributed evaluation infrastructure

At that point the benchmark dataset can be executed without modification to the evaluation pipeline.

## Implementation Notes

The evaluation module remains available through:

```bash
python -m rag_evaluation.evaluate
```

The generated report is written to:

```
rag_evaluation/report.json
```

The evaluation architecture is considered complete for Phase 4. Future work focuses on improving execution capacity rather than redesigning the evaluation framework.
