from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from src.latest_ai_development.vectorstore import VectorStore  # Import your custom VectorStore
import os

CHROMA_DIR = "vector_db"  # Changed to match your VectorStore path

def ingest_blog_text(blog_text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents([blog_text])
    
    # Initialize your custom VectorStore (local SentenceTransformer)
    vectorstore = VectorStore(persist_path=CHROMA_DIR)
    
    vectorstore.add_documents(
        texts=[chunk.page_content for chunk in chunks],
        metadatas=[{}] * len(chunks)  # Optional metadata
    )
    return f"Ingested {len(chunks)} chunks into vector DB"

def retrieve_similar_docs(query: str, k: int = 3):
    vectorstore = VectorStore(persist_path=CHROMA_DIR)
    results = vectorstore.search(query, k=k)
    return results if results else ["No relevant past context found."]