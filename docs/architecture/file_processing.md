# File Processing Architecture

## Overview

The file processing layer transforms uploaded learning resources into a normalized document representation that can be consumed by the retrieval pipeline.

Instead of treating every supported file format as plain text, each processor converts its source into a structured document composed of semantic blocks.

Every supported source ultimately becomes:

```
DocumentRepresentation
│
├── Document Author (Optional)
└── Document Blocks
```

This allows downstream systems to operate on a common representation regardless of the original document format.

The complete processing pipeline executes asynchronously using Celery.

---

# Design Goals

The processing architecture was designed around several principles:

- Support multiple document formats through a common interface.
- Preserve document structure whenever possible.
- Keep extraction independent from persistence.
- Separate document parsing from chunk generation.
- Allow new file formats to be added without changing the processing pipeline.
- Generate embeddings from semantic document blocks rather than raw files.

---

# Processing Pipeline

Every uploaded resource follows the same high-level workflow.

```
Upload
    ↓
File Type Detection
    ↓
Processor Selection
    ↓
Document Extraction
    ↓
Document Representation
    ↓
Document Chunking
    ↓
Embedding Generation
    ↓
Database Persistence
```

The retrieval layer never operates directly on uploaded files.

It only interacts with processed chunks stored in the database.

---

# Processing Flow

The complete workflow spans multiple architectural layers.

```
Route
    ↓
Upload Service
    ↓
Celery Task
    ↓
File Processor
    ↓
Repositories
    ↓
Database
```

Each layer owns a single responsibility.

---

# File Type Detection

The upload layer determines the processor using the uploaded source type.

Example:

```
notes.pdf

↓

FileTypes.PDF

↓

PDFProcessor
```

This converts external file formats into a common internal representation used throughout the backend.

---

# Processor Registry

Concrete processors are resolved through a registry.

```
FileType
    ↓
Processor Registry
    ↓
Concrete Processor
```

Supported processors include:

- PDF Processor
- DOCX Processor
- Markdown Processor
- Text Processor
- CSV Processor
- Image Processor
- YouTube Processor

Adding support for new formats only requires implementing and registering another processor.

---

# Document Representation

Every processor produces a common document representation.

```
DocumentRepresentation
│
├── author (optional)
│
└── blocks
      ├── type
      ├── text
      └── metadata
```

The representation preserves document semantics before any retrieval-specific processing occurs.

Processors no longer return plain text.

---

# Document Blocks

Every document is divided into logical blocks.

Current block types include:

- Paragraph
- Heading
- Table
- Code
- List
- OCR
- Transcript
- Description

Each block stores:

- semantic block type
- extracted text
- block-specific metadata

Metadata varies by source.

Examples include:

PDF

```
page
```

CSV

```
row_range
```

YouTube

```
start
end
```

The metadata intentionally remains flexible rather than forcing every document type into a fixed schema.

---

# OCR Support

Images are processed using OCR before entering the document representation.

```
Image
    ↓
OCR
    ↓
OCR Block
    ↓
Document Representation
```

OCR output is treated the same as any other document block.

---

# Document Chunking

After extraction, document blocks are converted into retrieval chunks.

The chunker operates on document structure rather than raw text.

Oversized blocks are tokenized and divided using the token-aware chunker while preserving metadata.

Certain block types remain intact.

Current non-splittable blocks include:

- Headings
- Tables

Every resulting chunk preserves the metadata of its originating block together with retrieval metadata such as token ranges and chunk indices.

---

# Embedding Generation

Each chunk is converted into a vector representation.

```
Chunks
    ↓
Embedding Model
    ↓
Embeddings
```

Embeddings are generated independently from document extraction.

Processors themselves never communicate with embedding providers.

---

# Persistence Separation

Processors never communicate directly with the database.

Instead they return a normalized document representation.

```
Processor
    ↓
Document Representation
    ↓
Document Chunker
    ↓
Repositories
    ↓
Database
```

This separation keeps extraction reusable and independently testable.

---

# Asynchronous Execution

Processing executes inside Celery workers.

Typical workflow:

```
Upload Request
    ↓
Upload Service
    ↓
Celery Task
    ↓
Document Extraction
    ↓
Document Chunking
    ↓
Embedding Generation
    ↓
Persistence
```

The upload request returns immediately while processing continues in the background.

---

# Supported Resource Types

Current supported sources include:

- Plain Text (.txt)
- Markdown (.md)
- Microsoft Word (.docx)
- PDF
- CSV
- Images (OCR)
- YouTube Videos

Every supported source ultimately produces the same document representation before entering retrieval.

---

# Error Handling

Processing failures remain isolated to the affected upload.

The processing task is responsible for:

- updating processing status
- recording sanitized error messages
- rolling back failed transactions
- preventing partial persistence

This ensures failed processing never leaves inconsistent database state.

---

# Extensibility

Supporting a new document type generally requires:

1. Add a new `FileType`.
2. Implement a processor.
3. Register the processor.

No changes are required to the chunker, embedding generation, or retrieval pipeline.

---

# Future Improvements

Potential future enhancements include:

- Structure-aware PDF parsing
- Better OCR pipelines
- Spreadsheet understanding
- Presentation parsing
- Audio transcription
- Multi-document ingestion
- Incremental document updates

These improvements extend the extraction layer without affecting downstream retrieval.

---

# Guiding Principle

Processors understand document formats.

The document representation preserves document structure.

The document chunker prepares content for retrieval.

Repositories persist processed chunks.

The retrieval pipeline operates only on normalized document chunks.