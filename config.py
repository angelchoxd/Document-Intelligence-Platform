OLLAMA_MODELS = {
    "Qwen3 4B": "qwen3:4b",
    "Llama 3.2 3B": "llama3.2:3b",
}

DEFAULT_LLM_MODEL = "qwen3:4b"

OLLAMA_MODEL = DEFAULT_LLM_MODEL

COLLECTION_NAME = "document_collection"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K_RESULTS = 3
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100