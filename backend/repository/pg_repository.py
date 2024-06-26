import uuid
from dataclasses import dataclass

from langchain.docstore.document import Document
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from persistence.database import Event as EventDB
from pydantic import ValidationError
from schemas.event import Event, Events, EventType
from shared.base import logger
from shared.settings import app_settings
from shared.ulid import ulid_as_uuid
from sqlalchemy import create_engine, delete, desc, insert, select, text
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
        self.event_type_to_store: dict[EventType, VectorStoreRetriever] = {
            EventType.EVENT: PGVector(
                collection_name="vector_collection_event",
                connection_string=con_string,
                embedding_function=self.embedding_model,
            ).as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": 0.2, "k": 1},
            ),
            EventType.RESTAURANT: PGVector(
                collection_name="vector_collection_restaurant",
                connection_string=con_string,
                embedding_function=self.embedding_model,
            ).as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": 0.2, "k": 1},
            ),
        }
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512)

    async def health(self) -> None:
        async with self._aengine.connect() as session:
            result = await session.execute(text("select 1"))
            one = result.fetchone()
            if one is not None and one[0] != 1:
                raise Exception('Should be 1 from "select 1"')

    def compile_table(self, table) -> str:  # noqa: ANN001
        return str(CreateTable(table.__table__).compile(dialect=postgresql.dialect()))

    def delete_events(self) -> None:
        logger.info("DELETING EVENTS!")
        with self._engine.connect() as session:
            session.execute(delete(EventDB))
            session.commit()

    def delete_embeddings(self) -> None:
        logger.info("DELETING EMBEDDING!")
        with self._engine.connect() as session:
            session.execute(
                text(
                    "delete from langchain_pg_collection where name in ('vector_collection_event', 'vector_collection_restaurant')"
                )
            )
            session.commit()

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
                        reviews=event.reviews,
                    )
                )
            session.commit()

    def get_event(self, id_: uuid.UUID) -> Event:
        with self._engine.connect() as session:
            row = session.execute(
                select(EventDB).where(EventDB.internal_id == id_)
            ).fetchone()
            return self._parse_event(row)

    def _parse_event(self, row: EventDB) -> Event:
        return Event(
            id=row.internal_id,
            type=row.type,
            restaurant_type=row.restaurant_type,
            name=row.name,
            description=row.description,
            link=row.link,
            img_link=row.img_link,
            price=row.price,
            address=row.address,
            lat=row.lat,
            lng=row.lng,
            time=None,
            distance=None,
        )

    def get_events(self) -> Events:
        with self._engine.connect() as session:
            rows = session.execute(select(EventDB)).fetchall()

        events = []
        for row in rows:
            try:
                events.append(self._parse_event(row))
            except ValidationError:
                logger.exception(f"failed to validate event from db, row: {row}")

        return Events(events=events)
