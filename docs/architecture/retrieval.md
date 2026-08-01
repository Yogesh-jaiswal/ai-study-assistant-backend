# Retrieval Architecture

## Overview

The retrieval pipeline is responsible for locating the most relevant information from a notebook before sending it to an AI model.

Instead of allowing the language model to answer directly from its own knowledge, the backend first retrieves relevant notebook content and injects that context into the prompt. This grounds every response in the user's uploaded material and reduces hallucinations.
The retrieval system is completely independent from the AI generation infrastructure.

Other AI features such as summaries, flashcards, quizzes, exams, and mind maps use the generic AI generation architecture described in [ai.md](ai.md) and do not depend on retrieval.

---

# Design Philosophy

The retrieval pipeline follows a staged architecture where every component owns exactly one responsibility.

```text
User Query
    ↓
Query Embedding
    ↓
Similarity Search
    ↓
Retrieved Chunks
    ↓
Context Assembly
    ↓
Prompt Builder
    ↓
AI Generator
    ↓
Citation Builder
    ↓
Final Response
```

Each stage only knows about its own responsibility.

For example:

- Embedding generation does not know how retrieval works.
- Retrieval does not know how prompts are built.
- Context assembly does not know how responses are generated.
- Citation generation does not know how retrieval is implemented.
- AI generation never receives citation information.

This separation allows every stage to evolve independently.

---

# Current Retrieval Pipeline

The current implementation performs the following steps:

1. Receive the user's question.
2. Generate a query embedding.
3. Perform similarity search.
4. Filter results using the configured similarity threshold.
5. Return the Top-K retrieved chunks.
6. Assemble the retrieved chunks into prompt-ready context.
7. Generate the AI response.
8. Build citations from the retrieved chunks.
9. Return both the response and citations.

Only notebook content participates in retrieval.

No external knowledge sources are currently used.

---

# Document Processing

Before retrieval, uploaded resources are converted into a structured document representation.

```text
Uploaded File
        ↓
Document Processor
        ↓
Document Representation
        ↓
Document Chunker
        ↓
Token Chunker (when required)
        ↓
Embedding Generation
        ↓
Vector Storage
```

Unlike the original implementation, retrieval no longer operates on plain text.

Every document processor produces a structured representation that preserves logical document blocks.

---

# Document Representation

Every uploaded resource is represented as:

```text
Document
│
├── Metadata
│
└── Blocks
      │
      ├── Paragraph
      ├── Heading
      ├── Table
      ├── OCR
      ├── Code
      ├── List
      ├── Transcript
      └── Description
```

Each block contains:

- Block type
- Block text
- Document-specific metadata

The metadata depends on the document source.

Examples include:

| Source | Metadata |
|---------|----------|
| PDF | page |
| CSV | row_range |
| YouTube | start, end |
| TXT | none |
| DOCX | none |
| Image | none |

The retrieval pipeline preserves this metadata throughout chunking, retrieval, and citation generation.

---

# Chunking

Chunking operates on document blocks instead of raw text.

Small blocks remain unchanged.

Large blocks are split using token-aware chunking while preserving the original block metadata.

Each produced chunk stores:

- chunk index
- block type
- block metadata
- chunk content

This allows retrieval to preserve document structure while remaining compatible with embedding model limits.

---

# Chunk Storage

Every chunk stores only the information required during retrieval.

```text
Chunk
├── upload_id
├── chunk_index
├── block_type
├── metadata
└── content
```

Embeddings are stored separately using a one-to-one relationship.

```text
Embedding
├── chunk_id
└── vector
```

Separating embeddings from chunk data keeps the document model lightweight while allowing future embedding model migrations.

---

# Embeddings

Both notebook chunks and user queries use the same embedding model.

Document workflow:

```text
Document
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Vector Storage
```

Query workflow:

```text
Question
    ↓
Embedding Generation
    ↓
Similarity Search
```

Using the same embedding model for both documents and queries ensures comparable vector representations.

---

# Similarity Search

Similarity search retrieves the most relevant chunks for a user query.

The retrieval service receives:

- User ID
- Notebook ID
- Query
- Top-K value

The retrieval layer:

- generates the query embedding
- performs vector similarity search
- filters low-confidence matches
- enforces notebook ownership
- returns retrieved chunks together with upload information and similarity scores

The retrieval service itself remains independent of prompt generation.

---

# Context Assembly

After retrieval, the selected chunks are assembled into prompt-ready context.

Current implementation:

```text
Chunk 1

---

Chunk 2

---

Chunk 3
```

The context assembler intentionally performs no ranking or modification.

Its only responsibility is converting retrieved chunks into prompt-ready text while preserving retrieval order.

---

# Prompt Generation

The prompt builder combines:

- system instructions
- user question
- assembled notebook context

The notebook context is treated as untrusted user content.

Instructions that appear inside uploaded documents are ignored and treated as ordinary notebook text.

---

# Citation Builder

After the AI response is generated, citations are constructed from the retrieved chunks.

Each citation combines:

- upload filename
- upload author
- upload source type
- document-specific metadata

Duplicate citations are removed before returning the response.

Current citation examples include:

```text
os.pdf
page: 9
```

or

```text
house_prices.csv
row_range: 0-50
```

The AI model never receives citation information.

Citation generation is entirely independent from response generation.

---

# Grounded Responses

The retrieval pipeline minimizes hallucinations by grounding every response in retrieved notebook content. The prompt explicitly instructs the language model to answer only from the supplied context and refuse when the required information is unavailable.

---

# Future Improvements

The current retrieval pipeline intentionally remains simple.

Potential future improvements include:

- Cross-encoder reranking
- Hybrid keyword + vector search
- Multi-query retrieval
- Context compression
- Parent-document retrieval
- Retrieval evaluation metrics
- Adaptive Top-K selection