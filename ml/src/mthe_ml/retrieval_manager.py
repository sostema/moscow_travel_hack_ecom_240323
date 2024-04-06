from typing import Any

from langchain.docstore.document import Document
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore, RedisStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .helper import get_pgvector_store


class RetrievalManager:
    def __init__(
        self,
    ):
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="cointegrated/rubert-tiny2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512)
        # self.parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, add_start_index=True)
        # self.child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
        self.store = get_pgvector_store(self.embedding_model, "retrieval_manager_test")
        # The storage layer for the parent documents
        self.retriever = self.store.as_retriever(search_type="mmr")

    def add_documents(self, documents: list[Document]):
        self.retriever.add_documents(documents)

    def retrieve_most_relevant_document(self, query: str) -> list[Document]:
        relevant_documents = self.retriever.get_relevant_documents(query)
        most_relevant = relevant_documents[0]
        return most_relevant

    def retrieve_relevant_documents(self, query: str) -> list[Document]:
        relevant_documents = self.retriever.get_relevant_documents(query)
        return relevant_documents
