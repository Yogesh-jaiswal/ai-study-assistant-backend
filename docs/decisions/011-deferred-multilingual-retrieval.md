# Decision 011: Deferred Multilingual Retrieval

## Decision

Use `all-MiniLM-L6-v2` as the default embedding model during Phase 4.

The document processing pipeline may extract multilingual content (for example, Hindi OCR output or non-English YouTube transcripts), but semantic retrieval is currently optimized for English.

## Reason

The project primarily targets educational documents that are expected to be written in English.

Using the English MiniLM model provides several practical advantages:

* Faster embedding generation
* Lower memory consumption
* Smaller model download size
* Better CPU performance on development hardware
* Excellent retrieval quality for English educational content

A multilingual embedding model significantly increases inference time and memory usage while providing limited benefit for the current project scope.

The backend architecture already supports changing the embedding model through configuration, allowing multilingual retrieval to be introduced later without modifying the retrieval pipeline.

## Current Behavior

The current pipeline behaves as follows:

* OCR extracts English and Hindi text when available.
* YouTube extraction prefers English transcripts, then English auto-generated transcripts, then falls back to the first available transcript.
* Retrieved multilingual content is still indexed.
* Retrieval quality for non-English documents is not guaranteed while using the English embedding model.

## Future Revisit Criteria

Consider switching to a multilingual embedding model if:

* Multilingual notebooks become a primary use case.
* International users become a target audience.
* OCR-generated documents become a major source of uploaded content.
* Retrieval quality for non-English content becomes a product requirement.
* Hardware or deployment infrastructure allows the additional inference cost.

## Implementation Notes

The embedding model is configurable through the application settings:

```env
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
```

A multilingual model can be enabled later by changing only this configuration value without requiring changes to the retrieval architecture.
