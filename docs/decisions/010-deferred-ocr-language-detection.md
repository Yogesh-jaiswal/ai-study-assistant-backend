# Decision 010: Deferred Dynamic OCR Language Detection

## Decision

Limit OCR extraction to English and Hindi during Phase 4.

Current OCR configuration:

- eng
- hin

## Reason

The current project primarily targets educational content expected to be written in English or Hindi.

Supporting dynamic language detection would require introducing additional infrastructure such as:

- OCR language detection
- Dynamic Tesseract language selection
- Multiple language package management
- OCR provider abstraction

While valuable for internationalization, these additions increase implementation complexity without improving the current learning objectives.

The current retrieval pipeline is optimized for English content. Hindi OCR and non-English transcripts are extracted when available, but retrieval quality for those languages is not guaranteed during Phase 4.

## Future Revisit Criteria

Consider implementing dynamic OCR language support if:

- Image uploads become a primary content source
- International language support becomes a product requirement
- Multiple OCR providers are introduced
- Automatic language detection is added to the document processing pipeline