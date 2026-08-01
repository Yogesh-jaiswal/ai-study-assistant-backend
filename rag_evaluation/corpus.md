# Artificial Intelligence Study Notes

## What is Artificial Intelligence?

Artificial Intelligence (AI) is a branch of computer science focused on building systems capable of performing tasks that normally require human intelligence.

Common AI capabilities include:

* Understanding language
* Recognizing images
* Making decisions
* Solving problems
* Learning from data

AI systems are used in healthcare, education, finance, transportation, and many other industries.

---

## Machine Learning

Machine Learning (ML) is a subset of Artificial Intelligence.

Instead of following explicitly programmed rules, machine learning models learn patterns from data.

The three primary learning paradigms are:

* Supervised Learning
* Unsupervised Learning
* Reinforcement Learning

Examples of machine learning applications include spam detection, recommendation systems, fraud detection, and image classification.

---

## Deep Learning

Deep Learning is a specialized area of Machine Learning based on artificial neural networks.

Deep learning models usually require:

* Large datasets
* High computational power
* GPUs for efficient training

Deep learning powers modern applications such as speech recognition, computer vision, and large language models.

---

## Natural Language Processing

Natural Language Processing (NLP) enables computers to understand and generate human language.

Typical NLP tasks include:

* Text summarization
* Machine translation
* Question answering
* Sentiment analysis
* Named entity recognition

Large Language Models (LLMs) are advanced NLP systems trained on massive text corpora.

---

## Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) combines information retrieval with language generation.

A typical RAG pipeline consists of:

1. User submits a question.
2. The question is converted into an embedding.
3. Similar document chunks are retrieved.
4. Retrieved context is injected into the prompt.
5. The language model generates a grounded response.

The main advantage of RAG is reducing hallucinations by grounding answers in external knowledge.

---

## Vector Embeddings

Embeddings convert text into dense numerical vectors.

Texts with similar meanings produce vectors that are close together in vector space.

Vector databases perform similarity search using these embeddings.

Common similarity metrics include:

* Cosine similarity
* Dot product
* Euclidean distance

---

## Chunking

Large documents are divided into smaller pieces called chunks before embeddings are generated.

Common chunking strategies include:

* Fixed-size chunking
* Sentence-aware chunking
* Token-aware chunking
* Document-aware chunking

Token-aware chunking respects the token limits of the embedding model while preserving overlapping context between neighboring chunks.

---

## Metadata

Metadata describes information about a document rather than its contents.

Examples include:

* Author
* File name
* Page number
* Heading
* Table location
* Source type

Metadata allows retrieval systems to generate accurate citations.

---

## Flask

Flask is a lightweight Python web framework.

Flask applications commonly use:

* Blueprints
* SQLAlchemy
* Jinja templates
* Request handlers
* Middleware

Flask is frequently used for REST APIs and backend services.

---

## PostgreSQL

PostgreSQL is an open-source relational database.

Features include:

* ACID compliance
* Transactions
* JSON support
* Indexing
* Extensions

The pgvector extension enables efficient vector similarity search inside PostgreSQL.

---

## Celery

Celery is a distributed task queue for Python.

It allows long-running work to execute asynchronously.

Typical Celery use cases include:

* File processing
* Email delivery
* Background AI generation
* Scheduled tasks

Celery commonly uses Redis as its message broker.

---

## Python

Python is a high-level programming language known for readability and simplicity.

Popular Python libraries include:

* Flask
* FastAPI
* NumPy
* Pandas
* PyTorch
* Scikit-learn

Python is widely used in backend development, data science, automation, and artificial intelligence.

---

## Summary

Artificial Intelligence includes Machine Learning, Deep Learning, and Natural Language Processing.

Modern AI systems frequently use Retrieval-Augmented Generation to answer questions using external knowledge.

A production RAG backend commonly combines:

* Document chunking
* Embedding generation
* Vector similarity search
* Context assembly
* Prompt generation
* Large language models

This architecture enables accurate, grounded responses while minimizing hallucinations.
