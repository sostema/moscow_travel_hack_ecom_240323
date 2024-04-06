from dataclasses import dataclass

from langchain.docstore.document import Document
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from shared.settings import app_settings
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine


@dataclass
class PgRepository:
    def __post_init__(self) -> None:
        self._aengine = create_async_engine(
            f"postgresql+asyncpg://{app_settings.pg_username}:{app_settings.pg_password}@"
            f"{app_settings.pg_host}:{app_settings.pg_port}/{app_settings.pg_database}",
        )
        con_string = (
            f"postgresql+psycopg2://{app_settings.pg_username}:{app_settings.pg_password}@"
            f"{app_settings.pg_host}:{app_settings.pg_port}/{app_settings.pg_database}"
        )
        self._engine = create_engine(con_string)

        self.embedding_model = SentenceTransformerEmbeddings(
            model_name="cointegrated/rubert-tiny2"
        )
        self.pg_vector = PGVector(
            collection_name="db_main",
            connection_string=con_string,
            embedding_function=self.embedding_model,
        )
        self.retriever = self.pg_vector.as_retriever()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512)

    async def health(self) -> None:
        async with self._aengine.connect() as session:
            result = await session.execute(text("select 1"))
            one = result.fetchone()
            if one is not None and one[0] != 1:
                raise Exception('Should be 1 from "select 1"')

    def create_embeddings_from_strings(
        self, documents: list[str], document_ids: list[int]
    ) -> None:
        splitted_documents = self.text_splitter.create_documents(
            documents,
            metadatas=[{"document_id": document_id} for document_id in document_ids],
        )
        self.retriever.add_documents(splitted_documents)

    def retrieve_relevant_documents(self, query: str) -> list[Document]:
        return self.retriever.get_relevant_documents(query)
