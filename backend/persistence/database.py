from shared.ulid import ulid_as_uuid
from sqlalchemy import BigInteger, Column, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

metadata_obj = MetaData(schema="public")

Base = declarative_base()
Base.metadata = metadata_obj


class Entity(Base):
    __abstract__ = True

    id_ = Column("id", BigInteger, primary_key=True)
    internal_id = Column(
        UUID(as_uuid=True), unique=True, default=ulid_as_uuid, nullable=False
    )
