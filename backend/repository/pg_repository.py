from dataclasses import dataclass

from langchain.docstore.document import Document
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from persistence.database import Event as EventDB
from pydantic import ValidationError
from schemas.event import Event, Events
from shared.base import logger
from shared.settings import app_settings
from shared.ulid import ulid_as_uuid
from sqlalchemy import create_engine, insert, select, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.schema import CreateTable


@dataclass
class PgRepository:
    def __post_init__(self) -> None:
        self._aengine = create_async_engine(
            f"postgresql+asyncpg://{app_settings.pg_username}:{app_settings.pg_password}@"
            f"{app_settings.pg_host}:{app_settings.pg_port}/{app_settings.pg_database}",
            pool_size=10,
            max_overflow=10,
        )
        con_string = (
            f"postgresql+psycopg2://{app_settings.pg_username}:{app_settings.pg_password}@"
            f"{app_settings.pg_host}:{app_settings.pg_port}/{app_settings.pg_database}"
        )
        self._engine = create_engine(con_string, pool_size=10, max_overflow=10)

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

    def compile_table(self, table) -> str:  # noqa: ANN001
        return str(CreateTable(table.__table__).compile(dialect=postgresql.dialect()))

    def insert_events(self, events: Events) -> None:
        with self._engine.connect() as session:
            for event in events.events:
                session.execute(
                    insert(EventDB).values(
                        type=event.type_,
                        restaurant_type=event.restaurant_type,
                        name=event.name,
                        description=event.description,
                        link=event.link,
                        img_link=event.img_link,
                        price=event.price,
                        address=event.address,
                        lat=event.lat,
                        lng=event.lng,
                        internal_id=ulid_as_uuid(),
                    )
                )
            session.commit()

    def get_events(self) -> Events:
        with self._engine.connect() as session:
            rows = session.execute(select(EventDB)).scalars().all()

        events = Events(events=[])
        for row in rows:
            try:
                events.events.append(Event.from_orm(row))
            except ValidationError:
                logger.error(f"failed to validate event from db, row: {row}")

        return events
