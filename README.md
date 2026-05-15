
🧠 RAGOps
A repository-aware AI debugging and architecture assistant built because I was tired of spending hours manually tracing APIs, controllers, services, and backend flows across large codebases just to understand how one feature worked.




🌍 The Real Problem Behind This Project
Every time I joined a new project or explored a large repository, the same thing happened:
* Routes were spread across multiple services
* Controllers referenced models buried deep inside backend folders
* Frontend flows triggered APIs indirectly through utility layers
* Important business logic was distributed across dozens of files
* Understanding one backend lifecycle meant opening 20+ tabs
Traditional code search wasn't enough.
Even when using AI tools, most assistants lacked repository-level understanding:
* they hallucinated APIs
* misunderstood architecture
* ignored service relationships
* failed to trace real backend flows
I realized most AI coding tools are very good at generating code — but not very good at understanding systems.
I wanted to build something that could actually understand a repository structurally, retrieve the correct engineering context, and explain how systems worked end-to-end.
So I built RAGOps.

✨ What RAGOps Does
RAGOps is a repository-aware AI engineering assistant built using Retrieval-Augmented Generation (RAG), vector search, reranking pipelines, and grounded LLM inference.
It allows developers to:
For Engineers
* 🔍 Ask architecture-level questions about a repository
* 🧠 Understand backend request lifecycles
* 🛠️ Debug systems using grounded code retrieval
* 🔗 Trace relationships across routes, controllers, models, and services
* 📚 Onboard into large codebases significantly faster
* ⚡ Retrieve semantically relevant code using vector search + reranking
For AI Engineering Workflows
* 🧩 Build repository-aware RAG pipelines
* 📦 Experiment with retrieval architectures
* 🚀 Explore modern embedding and reranking models
* 🧠 Improve grounded AI response quality
* ⚙️ Understand production-style AI infrastructure systems

🔄 How It Works — The Retrieval Flow

Developer asks question
        ↓
FastAPI backend receives query
        ↓
Repository chunks retrieved from ChromaDB
        ↓
Semantic similarity search using BAAI embeddings
        ↓
Cross-encoder reranker reorders retrieved chunks
        ↓
Context constructed from highest relevance files
        ↓
Groq-hosted LLM generates grounded response
        ↓
Developer receives architecture-aware answer

Unlike basic AI chatbots, RAGOps only answers using retrieved repository context — reducing hallucinations and improving engineering accuracy.

💡 Features In Detail
Repository-Aware Semantic Retrieval
The ingestion pipeline recursively processes repositories and generates semantic embeddings for:
* routes
* controllers
* database models
* frontend components
* utility modules
* service layers
Each chunk is stored with metadata such as:
* file path
* service name
* file type
This enables architecture-aware retrieval instead of naive keyword matching.

Modern Embedding Pipeline
Built using:
BAAI/bge-large-en-v1.5
I specifically chose this embedding model because:
* it performs extremely well on retrieval benchmarks
* handles technical/code-heavy content effectively
* produces high semantic similarity quality
* is widely adopted in modern production-grade RAG systems
The embedding model converts repository chunks into high-dimensional semantic vectors which are stored inside ChromaDB for similarity search.
Embedding Dimension
* 1024

Cross-Encoder Reranking
One major issue with vector search alone is noisy retrieval.
Initially I tried:
* manual scoring heuristics
* metadata boosting
* custom reranking logic
* handcrafted filtering systems
But modern RAG systems rely heavily on second-stage reranking models.
So I implemented:
BAAI/bge-reranker-base
The retriever first fetches semantically similar chunks.
Then the reranker:
* scores query-document relevance
* removes weaker matches
* reorders results for grounding quality
This significantly improved:
* architecture reasoning
* debugging accuracy
* backend flow tracing
* grounded generation quality

Grounded AI Responses
Instead of allowing the LLM to freely generate responses, RAGOps constructs prompts only from retrieved repository context.
This reduces:
* hallucinated APIs
* fake architecture explanations
* incorrect backend flows
* invented system behavior
Inference is handled using:
Groq API
Model:
* llama-3.1-8b-instant
I chose Groq because:
* extremely low latency
* fast inference speed
* lightweight setup
* ideal for rapid engineering workflows

🛠️ Tech Stack
Layer	Technology	Why I chose it
AI Orchestration	LlamaIndex	Modern retrieval framework with modular retrieval pipelines
Backend API	FastAPI	High-performance async Python backend
Vector Database	ChromaDB	Lightweight persistent vector storage
Embeddings	BAAI/bge-large-en-v1.5	Strong retrieval benchmark performance
Reranker	BAAI/bge-reranker-base	Cross-encoder precision reranking
LLM Inference	Groq API	Ultra-fast hosted inference
LLM	Llama 3.1 8B Instant	Fast grounded response generation
Backend Runtime	Uvicorn	ASGI production server
Validation	Pydantic	Structured API request validation
🗂️ Project Structure

ragops/
│
├── app.py                     # FastAPI server entrypoint
├── retrieval_engine.py        # Retrieval + reranking pipeline
├── ingest.py                  # Repository ingestion pipeline
├── debug_agent.py             # CLI debugging assistant
├── requirements.txt
│
├── chroma_db/                 # Persistent vector database
│
└── repos/                     # Ingested repositories
    ├── frontend/
    ├── backend/
    └── recommendation/


🚀 Running Locally
Prerequisites
* Python 3.9+
* Groq API Key
* Virtual Environment

Step 1 — Clone Repository

git clone https://github.com/Arjun-tech-lab/RAGops.git
cd ragops


Step 2 — Create Virtual Environment

python -m venv venv
source venv/bin/activate


Step 3 — Install Dependencies

pip install -r requirements.txt


Step 4 — Configure Environment Variables
Create .env

GROQ_API_KEY=your_groq_api_key


Step 5 — Ingest Repository

python ingest.py

This:
* chunks repository files
* generates embeddings
* stores vectors inside ChromaDB

Step 6 — Start FastAPI Server

uvicorn app:app --reload

Swagger Docs:

http://127.0.0.1:8000/docs


🔑 API Endpoints
Method	Endpoint	Description
GET	/	Health check
POST	/ask	Repository-aware AI query
Example Request:

{
  "question": "Explain the order creation flow"
}


🧪 What I Learned Building This
Retrieval Is Much Harder Than It Looks
Initially I tried building retrieval manually:
* metadata filtering
* handcrafted reranking
* custom scoring systems
* manual weighting heuristics
But I quickly realized modern RAG systems rely heavily on:
* stronger embedding models
* retrieval orchestration frameworks
* second-stage reranking
* better context construction
This project pushed me toward modern AI infrastructure tooling instead of trying to reinvent retrieval systems from scratch.

Vector Search Alone Is Not Enough
Semantic similarity retrieval works surprisingly well for simple queries.
But architecture-heavy engineering questions require:
* reranking
* broader contextual retrieval
* repository-aware chunking
* better retrieval orchestration
This was one of the biggest engineering lessons from the project.

AI Engineering Feels More Like Backend Engineering Than ML
Building RAGOps involved:
* API design
* vector database management
* retrieval orchestration
* backend infrastructure
* latency considerations
* context pipelines
* deployment architecture
It felt much closer to systems engineering than traditional machine learning experimentation.

🔮 What I'd Build Next
* LangGraph-based agent workflows
* Multi-hop repository reasoning
* Graph-based dependency traversal
* Hybrid BM25 + vector retrieval
* AST-aware chunking
* Conversational memory
* Frontend chat interface
* Cloud deployment pipeline

💡 Reflections
Most AI coding assistants generate code.
I wanted to build something that could understand systems.
RAGOps was my attempt at combining backend engineering, retrieval systems, vector search, reranking pipelines, and grounded AI reasoning into a developer-focused workflow.
Building it taught me that the hardest part of AI systems is not generation — it's retrieval quality, orchestration, and architecture understanding.

👤 Author
Arjun Indavara CS Undergrad @ Dayananda Sagar College of Engineering, Bengaluru Class of 2027

