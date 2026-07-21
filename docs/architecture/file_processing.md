# File Processing Architecture

## Overview

The file processing layer is responsible for transforming uploaded learning resources into a normalized representation that can be consumed by the retrieval pipeline.

Rather than treating every supported file format differently, the backend converts every resource into a common processed representation consisting of:

* Cleaned text
* Chunks
* Embeddings

This allows the retrieval layer to remain completely independent of the original document format.

The file processing pipeline is executed asynchronously using Celery.

---

## Design Goals

The processing architecture follows these principles:

* Support multiple document formats through a common interface.
* Normalize every resource into the same internal representation.
* Keep extraction independent from persistence.
* Make new file formats easy to introduce.
* Isolate format-specific logic.
* Reuse the same retrieval pipeline regardless of document type.

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

Text Extraction

↓

Text Cleaning

↓

Chunk Generation

↓

Embedding Generation

↓

Database Persistence
```

The retrieval layer only operates on the processed output and never interacts with raw uploaded files.

---

# Processing Flow

The complete processing workflow spans multiple architectural layers.

```
Route

↓

Upload Service

↓

Celery Task

↓

File Processor

↓

Processed File

↓

Repositories

↓

Database
```

Each component owns a single responsibility.

---

# File Type Detection

The upload layer determines the document type before processing begins.

Detection is performed using the uploaded file extension.

Example:

```
notes.pdf

↓

.pdf

↓

FileTypes.PDF
```

This step converts external file formats into an internal file type representation used throughout the backend.

---

# Processor Registry

After identifying the file type, processing is delegated through a registry.

```
FileType

↓

Processor Registry

↓

Concrete Processor
```

Example:

```
FileTypes.PDF
        ↓
PDFProcessor

FileTypes.DOCX
        ↓
DOCXProcessor

FileTypes.IMAGE
        ↓
ImageProcessor
```

The registry removes conditional logic from the processing pipeline and allows new processors to be added without modifying existing orchestration code.

---

# Processor Architecture

Every processor implements the same processing interface.

Examples include:

* PDF Processor
* DOCX Processor
* Markdown Processor
* Text Processor
* CSV Processor
* Image Processor
* YouTube Processor

Each processor is responsible only for understanding its own document format.

The orchestration layer remains unaware of format-specific implementation details.

---

# Normalized Output

Regardless of the original resource, every processor produces the same logical result.

```
Processed File

├── cleaned_text
├── chunks
└── embeddings
```

This normalized representation allows every downstream system to operate on a common structure.

The retrieval pipeline therefore does not need to distinguish between PDFs, images, markdown documents, or videos.

---

# OCR Support

Images are treated as first-class learning resources.

The image processor performs Optical Character Recognition (OCR) before entering the normal processing pipeline.

```
Image

↓

OCR

↓

Extracted Text

↓

Chunk Generation

↓

Embeddings
```

Once OCR completes, images become indistinguishable from text-based documents.

---

# Chunk Generation

After text extraction and cleaning, documents are divided into smaller semantic units.

```
Cleaned Text

↓

Chunk Generator

↓

Chunks
```

Chunking prepares documents for embedding generation and retrieval.

The current implementation uses the project's retrieval pipeline for chunk generation.

Future chunking strategies may evolve independently without affecting document processors.

---

# Embedding Generation

Each generated chunk is converted into a vector representation.

```
Chunks

↓

Embedding Model

↓

Embeddings
```

Embeddings are stored separately from chunks and power semantic retrieval.

Processors themselves never generate or persist embeddings directly.

---

# Persistence Separation

Processors never communicate with the database.

Instead, processors return a normalized processed representation.

```
Processor

↓

Processed File

↓

Repositories

↓

Database
```

This separation provides several advantages:

* Easier testing
* Better modularity
* Clear separation of concerns
* Reusable processors

Processing logic remains independent from persistence.

---

# Asynchronous Execution

Processing is performed asynchronously using Celery.

This prevents expensive extraction and embedding operations from blocking HTTP requests.

Typical workflow:

```
Upload Request

↓

Upload Service

↓

Celery Task

↓

Extraction

↓

Chunking

↓

Embedding

↓

Persistence
```

The client receives immediate feedback while processing continues in the background.

---

# Supported Resource Types

Each processed upload is assigned a resource purpose.

Current purposes include:

- Notes
- Reference Papers

The processing pipeline itself is identical regardless of purpose. Resource purpose is consumed later during AI context assembly rather than during file extraction.

The current processing pipeline supports:

* Plain Text (.txt)
* Markdown (.md)
* Microsoft Word (.docx)
* PDF Documents
* CSV Files
* Images (OCR)
* YouTube Videos

Every supported source is ultimately converted into the same normalized representation before downstream AI workflows.

---

# Error Handling

Failures during processing are isolated to the affected upload.

The processing task is responsible for:

* Updating processing status
* Recording sanitized error messages
* Rolling back failed transactions
* Preventing partial persistence

This ensures processing failures do not leave inconsistent database state.

---

# Extensibility

Adding support for a new resource type generally requires:

1. Define a new FileType.
2. Implement a processor.
3. Register the processor.
4. Register the upload extension if applicable.

The orchestration pipeline remains unchanged.

This minimizes modifications when introducing additional document sources.

---

# Future Improvements

Potential future enhancements include:

* Document-aware chunking
* Token-aware chunking
* Advanced OCR
* Table extraction
* Presentation parsing
* Spreadsheet structure understanding
* Audio transcription
* Multi-document ingestion
* Incremental document updates

These improvements extend the processing layer while preserving the existing pipeline.

---

# Guiding Principle

Every supported resource should be transformed into normalized text before entering the retrieval pipeline.

Format-specific complexity belongs inside processors.

Extraction belongs to the processing layer.

Persistence belongs to repositories.

Retrieval operates only on normalized processed content.