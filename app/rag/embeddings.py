from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
)