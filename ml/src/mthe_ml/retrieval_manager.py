from langchain.docstore.document import Document
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .configs import gigachat_settings, pgvector_settings


class RetrievalManager:
    def __init__(self):
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="cointegrated/rubert-tiny2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512)
        connection_string = f"postgresql+psycopg2://db_main:{pgvector_settings.pwd}@{pgvector_settings.host}:5432/db_main"
        store = PGVector(
            collection_name=pgvector_settings.connection_name,
            connection_string=connection_string,
            embedding_function=self.embedding_model,
        )
        self.retriever = store.as_retriever()

    def create_embeddings_from_strings(
        self, documents: list[str], document_ids: list[int]
    ):
        splitted_documents = self.text_splitter.create_documents(
            documents,
            metadatas=[{"document_id": document_id} for document_id in document_ids],
        )
        self.retriever.add_documents(splitted_documents)

    def retrieve_relevant_documents(self, query: str) -> list[Document]:
        relevant_documents = self.retriever.get_relevant_documents(query)
        return relevant_documents
