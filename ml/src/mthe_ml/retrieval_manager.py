from typing import Any

from langchain.docstore.document import Document
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.retrievers import EnsembleRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer

from .helper import get_pgvector_store


class RetrievalManager:
    def __init__(
        self,
    ):
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="cointegrated/rubert-tiny2"
        )
        self.tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512)
        self.store = get_pgvector_store(self.embedding_model, "retrieval_manager_test")
        self.retriever = self.store.as_retriever(search_type="mmr")

    def add_documents_from_strings(
        self, documents: list[str], metadatas: list[dict[str, Any]]
    ):
        splitted_documents = self.text_splitter.create_documents(
            documents,
            metadatas=metadatas,
        )
        self.store.add_documents(splitted_documents)

    def add_documents(self, documents: list[Document]):
        splitted_documents = self.text_splitter.split_documents(documents)
        self.store.add_documents(splitted_documents)

    def retrieve_most_relevant_document(self, query: str) -> list[Document]:
        relevant_documents = self.retriever.get_relevant_documents(query)
        most_relevant = relevant_documents[0]
        return most_relevant

    def retrieve_relevant_documents(self, query: str) -> list[Document]:
        relevant_documents = self.retriever.get_relevant_documents(query)
        return relevant_documents
