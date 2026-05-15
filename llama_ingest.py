import chromadb

from llama_index.core import (
    SimpleDirectoryReader,
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
# LOAD DOCUMENTS
# =====================================================

documents = SimpleDirectoryReader(
    "./repos",
    recursive=True,
    exclude=[
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.svg",
        "*.mp4",
        "*.lock"
    ]
).load_data()


# =====================================================
# CHROMA DB
# =====================================================

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

chroma_collection = chroma_client.get_or_create_collection(
    "project_collection_v2"
)

vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)


# =====================================================
# BUILD INDEX
# =====================================================

index = VectorStoreIndex.from_documents(

    documents,

    storage_context=storage_context,

    embed_model=embed_model
)


print("\nINGESTION COMPLETE")