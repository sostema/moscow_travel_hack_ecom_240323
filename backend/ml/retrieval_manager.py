from langchain.docstore.document import Document
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from repository.pg_repository import PgRepository
from schemas.event import EventType


class RetrievalManager:
    def __init__(self, pg_repository: PgRepository):
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="cointegrated/rubert-tiny2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512)
        # self.parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, add_start_index=True)
        # self.child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
        self.pg_repository = pg_repository

    def add_documents(self, event_type: EventType, documents: list[Document]):
        self.pg_repository.event_type_to_store[event_type].add_documents(documents)

    def retrieve_most_relevant_document(
        self, event_type: EventType, query: str
    ) -> Document | None:
        relevant_documents = self.pg_repository.event_type_to_store[
            event_type
        ].get_relevant_documents(query)

        if len(relevant_documents) == 0:
            return None

        return relevant_documents[0]

    def retrieve_relevant_documents(
        self, event_type: EventType, query: str
    ) -> list[Document]:
        relevant_documents = self.pg_repository.event_type_to_store[
            event_type
        ].get_relevant_documents(query)
        return relevant_documents
