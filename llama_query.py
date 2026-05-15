import chromadb

from sentence_transformers import CrossEncoder

from llama_index.core import (
    VectorStoreIndex,
    StorageContext
)

from llama_index.embeddings.huggingface import (
    HuggingFaceEmbedding
)

from llama_index.vector_stores.chroma import (
    ChromaVectorStore
)


# =====================================================
# EMBEDDINGS
# =====================================================

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5"
)


# =====================================================
# RERANKER
# =====================================================

reranker = CrossEncoder(
    "BAAI/bge-reranker-base"
)


# =====================================================
# CHROMA SETUP
# =====================================================

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

chroma_collection = chroma_client.get_collection(
    "project_collection_v2"
)

vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)


# =====================================================
# LOAD INDEX
# =====================================================

index = VectorStoreIndex.from_vector_store(

    vector_store,

    embed_model=embed_model
)


retriever = index.as_retriever(
    similarity_top_k=15
)


# =====================================================
# QUERY
# =====================================================

query = input("Ask question: ")


# =====================================================
# RETRIEVE
# =====================================================

nodes = retriever.retrieve(query)


# =====================================================
# RERANK
# =====================================================

pairs = []

for node in nodes:

    pairs.append([
        query,
        node.text
    ])


scores = reranker.predict(pairs)


# =====================================================
# SORT RESULTS
# =====================================================

reranked = sorted(

    zip(scores, nodes),

    key=lambda x: x[0],

    reverse=True
)


# =====================================================
# PRINT RESULTS
# =====================================================

for score, node in reranked[:5]:

    print("\n")
    print("=" * 80)

    print(f"SCORE: {score}")

    print("\n")

    print(node.metadata.get("file_path"))

    print("\n")

    print(node.text[:1500])