# src/blog_writer_crewai/tools/vectorstore.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction  
import os

class VectorStore:
    def __init__(self, persist_path="./vector_db"):
        import chromadb
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

        self.client = chromadb.PersistentClient(path=persist_path)
        self.embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name="blog_knowledge",
            embedding_function=self.embedding_function
        )

    def add_documents(self, texts: list[str], metadatas: list[dict]):
        ids = [f"doc_{i}" for i in range(len(texts))]
        self.collection.add(documents=texts, metadatas=metadatas, ids=ids)

    def search(self, query: str, k: int = 3):
        results = self.collection.query(query_texts=[query], n_results=k)
        documents = results.get("documents", [[]])[0]
        if not documents:
         return ["No relevant documents found."]
        return results["documents"][0]

    def persist(self):
        pass