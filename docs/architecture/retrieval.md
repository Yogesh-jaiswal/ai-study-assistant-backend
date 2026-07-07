# Retrieval Architecture

## Purpose

The retrieval pipeline is responsible for locating the most relevant information from a notebook before sending it to an AI model.

Instead of allowing the language model to answer directly from its own knowledge, the backend first retrieves relevant notebook content and injects that context into the prompt. This improves factual accuracy while grounding responses in the user's uploaded material.

The retrieval system is designed as an independent backend capability dedicated to notebook question answering.
It is responsible for locating the most relevant notebook content before passing that context to the AI generator.

Other AI features such as summaries, flashcards, quizzes, and future learning workflows use the independent AI generation architecture described in [ai.md](ai.md) and do not currently depend on the retrieval pipeline.

---

# Design Philosophy

The retrieval pipeline follows a staged architecture where each component has a single responsibility.

```text
User Query
    ↓
Generate Query Embedding
    ↓
Similarity Search
    ↓
Top-K Relevant Chunks
    ↓
Context Assembly
    ↓
Generator
    ↓
Prompt Builder
    ↓
AI Engine
    ↓
Final Response
```

Each stage only knows about its immediate responsibility.

For example:

* Embedding generation does not know how retrieval works.
* Retrieval does not know how prompts are built.
* Context assembly does not know how the AI model generates responses.
* AI generation does not know how vectors were retrieved.

This separation allows every stage to evolve independently.

---

# Current Retrieval Pipeline

The current implementation performs the following steps:

1. Receive the user's question.
2. Generate an embedding for the question.
3. Perform vector similarity search.
4. Filter results using a minimum similarity threshold.
5. Return the Top-K most relevant chunks.
6. Assemble retrieved chunks into a single context block.
7. Send the context to the AI generator.
8. Generate the grounded response.

Only notebook content participates in retrieval.

No external knowledge sources are currently used.

---

# Document Chunking

Uploaded documents are divided into smaller semantic chunks before embeddings are generated.

The current implementation uses sentence-aware chunking based on NLTK.

Configuration:

* Sentence tokenizer: `nltk.sent_tokenize`
* Default maximum sentences per chunk: **3**
* Default overlap: **1 sentence**

The overlap improves retrieval continuity by preserving context between neighboring chunks.

---

# Chunk Metadata

Each chunk currently stores only the metadata required for retrieval.

```text
Chunk
├── chunk_id
├── upload_id
├── chunk_index
└── content
```

Embeddings are stored separately using a one-to-one relationship.

```text
Embedding
├── chunk_id
└── vector
```

Keeping embeddings separate avoids mixing large vector data with document metadata while simplifying future embedding model migrations.

---

# Embeddings

Both notebook chunks and user queries use the same embedding model.

Current workflow:

```text
Document
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Vector Storage
```

For user queries:

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

Similarity search is performed against the vector database.

The retrieval service currently receives:

* User ID
* Notebook ID
* Query
* Top-K value

The retrieval layer filters results using a minimum similarity threshold before returning the most relevant chunks.

Notebook ownership is always enforced before retrieval to prevent cross-user access.

---

# Context Assembly

After retrieval, the selected chunks are assembled into a single context block.

Current implementation:

```text
Chunk 1

---

Chunk 2

---

Chunk 3
```

The current assembler intentionally remains simple.

Its only responsibility is combining retrieved chunks into a prompt-ready context while preserving retrieval order.

---

# Grounded Responses

The retrieval pipeline is designed to minimize hallucinations.

Rather than allowing unrestricted generation, AI prompts explicitly instruct the model to answer using the supplied notebook context.

If relevant information cannot be found, the AI should acknowledge the absence of supporting context instead of inventing facts.

---

# Future Improvements

The retrieval architecture is intentionally extensible.

Planned improvements include:

* Advanced chunk metadata
* Token-aware chunking
* Metadata-aware context assembly
* Source citations
* Retrieval evaluation metrics

These improvements will enhance retrieval quality without requiring architectural changes to the overall pipeline.