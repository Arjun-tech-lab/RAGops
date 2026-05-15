# RAGOps 🧠
### *Repository-Aware AI Debugging & Architecture Assistant*

> Built because tracing a single backend feature across 20+ files, spread across routes, controllers, services, and models, shouldn't take half a workday.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-7C3AED?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PC9zdmc+&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B35?style=flat&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat&logoColor=white)
![Llama](https://img.shields.io/badge/Llama_3.1-0467DF?style=flat&logo=meta&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-2D9CDB?style=flat&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)

---

## The Problem

Most AI coding assistants are excellent at **generating** code.  
Almost none of them are good at **understanding systems.**

When you join a large codebase or explore an unfamiliar repository, the same friction shows up every time:

- Routes are scattered across multiple services
- Controllers reference models buried deep in nested folders
- Frontend flows trigger APIs indirectly through utility layers
- Business logic is distributed across dozens of files
- Understanding one backend lifecycle means opening 20+ tabs

Traditional search doesn't solve this. Even AI tools fall short — they hallucinate APIs, misread architecture, ignore service relationships, and can't trace real backend flows.

**RAGOps fixes that.**

---

## What It Does

RAGOps is a **repository-aware AI engineering assistant** built using Retrieval-Augmented Generation (RAG), semantic vector search, cross-encoder reranking, and grounded LLM inference.

It allows developers to:

- Ask architecture-level questions about a codebase in plain English
- Trace backend request lifecycles end-to-end
- Understand relationships between routes, controllers, models, and services
- Debug systems using grounded code retrieval — not hallucinated guesses
- Onboard into unfamiliar repositories significantly faster

---

## How It Works

```
Developer asks a question
         │
         ▼
FastAPI backend receives query
         │
         ▼
ChromaDB retrieves repository chunks
         │
         ▼
BAAI/bge-large-en-v1.5 performs semantic similarity search
         │
         ▼
BAAI/bge-reranker-base reorders results by relevance
         │
         ▼
Context constructed from highest-relevance files only
         │
         ▼
Groq-hosted Llama 3.1 generates a grounded, sourced response
         │
         ▼
Developer receives architecture-aware answer
```

Unlike standard AI chatbots, **RAGOps only answers using retrieved repository context** — dramatically reducing hallucinations and improving engineering accuracy.

---

## Architecture

### Repository Ingestion
The ingestion pipeline recursively processes a repository and generates semantic embeddings for:

| Component | What's Indexed |
|-----------|---------------|
| Routes | API definitions and endpoint handlers |
| Controllers | Business logic and request handling |
| Models | Database schemas and data structures |
| Services | Core application logic and utilities |
| Frontend | Components and UI interaction flows |

Each chunk is stored in ChromaDB with metadata: `file_path`, `service_name`, `file_type` — enabling architecture-aware retrieval instead of naive keyword matching.

---

### Embedding Pipeline
**Model:** `BAAI/bge-large-en-v1.5` | **Embedding Dimension:** 1024

Chosen for:
- Top-tier performance on retrieval benchmarks
- Strong handling of technical and code-heavy content
- High semantic similarity quality across domain-specific terminology
- Widely adopted in production-grade RAG systems

---

### Cross-Encoder Reranking
**Model:** `BAAI/bge-reranker-base`

Vector search alone produces noisy results on architecture-level questions. A second-stage reranker fixes this:

1. Retriever fetches semantically similar chunks
2. Reranker scores query-document relevance precisely
3. Weak matches are filtered out
4. Results are reordered for maximum grounding quality

This meaningfully improved reasoning across backend flow tracing, debugging accuracy, and architecture understanding.

---

### Grounded LLM Inference
**Provider:** Groq API | **Model:** `llama-3.1-8b-instant`

Prompts are constructed **only from retrieved repository context.** The LLM cannot freely generate — it must reason from actual code. This eliminates hallucinated APIs, fake architecture explanations, and invented system behavior.

Groq was chosen for ultra-low latency inference, ideal for rapid engineering workflows.

---

## Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| AI Orchestration | LlamaIndex | Modular retrieval pipelines |
| Backend API | FastAPI | High-performance async Python |
| Vector Database | ChromaDB | Lightweight persistent vector storage |
| Embeddings | BAAI/bge-large-en-v1.5 | Strong retrieval benchmark scores |
| Reranker | BAAI/bge-reranker-base | Cross-encoder precision reranking |
| LLM Inference | Groq API | Ultra-fast hosted inference |
| LLM | Llama 3.1 8B Instant | Grounded response generation |
| Server Runtime | Uvicorn | ASGI production server |
| Validation | Pydantic | Structured API request validation |

---

## Project Structure

```
ragops/
├── app.py                  # FastAPI server entrypoint
├── retrieval_engine.py     # Retrieval + reranking pipeline
├── ingest.py               # Repository ingestion pipeline
├── debug_agent.py          # CLI debugging assistant
├── requirements.txt
│
├── chroma_db/              # Persistent vector database
│
└── repos/                  # Ingested repositories
    ├── frontend/
    ├── backend/
    └── recommendation/
```

---

## Getting Started

**Prerequisites:** Python 3.9+, Groq API Key

```bash
# 1. Clone the repository
git clone https://github.com/Arjun-tech-lab/RAGops.git
cd ragops

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
echo "GROQ_API_KEY=your_groq_api_key" > .env

# 5. Ingest your repository
python ingest.py

# 6. Start the server
uvicorn app:app --reload
```

Swagger docs available at: `http://127.0.0.1:8000/docs`

---

## API

**`POST /ask`** — Query the repository-aware assistant

```json
{
  "question": "Explain the order creation flow"
}
```

**`GET /`** — Health check

---

## Engineering Lessons

**Retrieval is harder than it looks.**  
I started with manual scoring heuristics, metadata boosting, and handcrafted filtering. None of it scaled. Modern RAG systems work because of strong embedding models, retrieval orchestration frameworks, and second-stage reranking — not custom logic.

**Vector search alone isn't enough.**  
Semantic similarity works well for simple queries. Architecture-level engineering questions need reranking, broader contextual retrieval, and repository-aware chunking.

**AI engineering feels more like backend engineering than ML.**  
Building RAGOps involved API design, vector database management, retrieval orchestration, latency optimization, and context pipeline architecture. Far closer to systems engineering than model training.

---

## What's Next

- [ ] Hybrid BM25 + vector retrieval
- [ ] AST-aware repository chunking
- [ ] Multi-hop repository reasoning
- [ ] LangGraph-based agent workflows
- [ ] Graph-based dependency traversal
- [ ] Conversational memory across sessions
- [ ] Frontend chat interface
- [ ] Cloud deployment pipeline

---

## Author

**Arjun Indavara**  
CS Undergrad · Dayananda Sagar College of Engineering, Bengaluru · Class of 2027

[![GitHub](https://img.shields.io/badge/GitHub-Arjun--tech--lab-181717?style=flat&logo=github)](https://github.com/Arjun-tech-lab)

---

*The hardest part of AI systems is not generation — it's retrieval quality, orchestration, and architecture understanding.*
