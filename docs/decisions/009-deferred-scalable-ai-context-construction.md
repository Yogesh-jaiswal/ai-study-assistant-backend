# Decision 9: Deferred Scalable AI Context Construction

## Decision

Do not implement scalable context-construction strategies during Phase 4.

Notebook-wide AI features will continue building context by concatenating the raw text of the selected uploads.

## Reason

The current implementation provides a simple, predictable, and maintainable architecture that is sufficient for the project's expected notebook sizes.

Implementing scalable context construction would introduce significant architectural complexity, including techniques such as:

- Hierarchical (Map-Reduce) summarization
- Recursive document summarization
- Context compression
- Semantic chunk merging
- Dynamic context budgeting

These techniques primarily address very large notebooks and production-scale deployments rather than the current learning-oriented project.

Additionally, chunk-based reconstruction is intentionally avoided because document chunks contain overlap for retrieval quality, making them unsuitable for rebuilding the original document efficiently.

## Future Revisit Criteria

Revisit this decision if:

- Notebook size regularly exceeds model context limits.
- Multiple AI features begin sharing notebook-wide context generation.
- AI inference costs become a concern.
- The application targets production-scale usage.
- Hierarchical or incremental notebook summaries become necessary.