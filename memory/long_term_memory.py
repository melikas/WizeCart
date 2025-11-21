"""Long-term memory using a vectorstore (FAISS/Chromadb) via LangChain's VectorStoreMemory.

This module provides a wrapper with embedding placeholder and compaction.
It includes fallbacks so the demo can run even if LangChain/FAISS aren't
installed yet. Replace with production vectorstore and embeddings as needed.
"""
import os
from real_time_shopping_assistant.config.settings import settings

try:
    from langchain.embeddings.base import Embeddings
    from langchain.memory import VectorStoreRetrieverMemory
    from langchain.vectorstores import FAISS
    # OpenAIEmbeddings could be used if keys provided
    from langchain.embeddings.openai import OpenAIEmbeddings  # type: ignore
    _HAS_LANGCHAIN = True
except Exception:
    _HAS_LANGCHAIN = False


class DummyEmbeddings:
    """Placeholder embedding implementation for demo/testing."""
    def __init__(self):
        pass

    def embed_documents(self, texts):
        # Very naive embedding: use length only (not for production)
        return [[float(len(t))] for t in texts]

    def embed_query(self, text):
        return [float(len(text))]


class DummyVectorStore:
    def __init__(self):
        self.docs = []

    @classmethod
    def from_texts(cls, texts, embedding):
        vs = cls()
        vs.docs = list(texts)
        return vs

    def as_retriever(self):
        # Simple retriever returning stored docs
        class Retriever:
            def __init__(self, docs):
                self.docs = docs

            def get_relevant_documents(self, query: str):
                return self.docs

        return Retriever(self.docs)


def create_vectorstore_and_memory():
    if _HAS_LANGCHAIN:
        emb = DummyEmbeddings()  # replace with OpenAIEmbeddings() in prod
        vs = FAISS.from_texts([], emb)
        memory = VectorStoreRetrieverMemory(retriever=vs.as_retriever(), memory_key="long_term")
        return vs, memory
    else:
        emb = DummyEmbeddings()
        vs = DummyVectorStore.from_texts([], emb)
        # Minimal memory object with retriever attribute
        class SimpleMemory:
            def __init__(self, retriever, memory_key="long_term"):
                self.retriever = retriever
                self.memory_key = memory_key

        memory = SimpleMemory(retriever=vs.as_retriever(), memory_key="long_term")
        return vs, memory


# expose factory
vectorstore, long_term_memory = create_vectorstore_and_memory()
