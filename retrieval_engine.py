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
# EMBEDDING MODEL
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
# CHROMA DB
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
    similarity_top_k=5
)


# =====================================================
# SEARCH FUNCTION
# =====================================================

def search_project(query):

    # ---------------------------------------------
    # RETRIEVE
    # ---------------------------------------------

    nodes = retriever.retrieve(query)


    # ---------------------------------------------
    # BUILD RERANK PAIRS
    # ---------------------------------------------

    pairs = []


    for node in nodes:

        pairs.append([
            query,
            node.text
        ])


    # ---------------------------------------------
    # RERANK
    # ---------------------------------------------

    scores = reranker.predict(pairs)


    # ---------------------------------------------
    # SORT RESULTS
    # ---------------------------------------------

    reranked = sorted(

        zip(scores, nodes),

        key=lambda x: x[0],

        reverse=True
    )


    # ---------------------------------------------
    # FORMAT RESULTS
    # ---------------------------------------------

    final_results = []


    for score, node in reranked[:3]:

        final_results.append({

            "score": float(score),

            "document": node.text,

            "metadata": {

    "path": node.metadata.get(
        "file_path"
    ),

    "type": node.metadata.get(
        "type"
    ),

    "service": node.metadata.get(
        "service"
    )
}
        })


    return final_results