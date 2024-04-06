from shared.ulid import ulid_as_uuid
from sqlalchemy import DECIMAL, FLOAT, TEXT, BigInteger, Column, MetaData
from sqlalchemy.dialects.postgresql import ARRAY, UUID
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


class Event(Entity):
    __tablename__ = "event"

    type_ = Column("type", TEXT)
    restaurant_type = Column(ARRAY(TEXT))
    reviews = Column(ARRAY(TEXT))
    name = Column(TEXT)
    description = Column(TEXT)
    link = Column(TEXT)
    img_link = Column(TEXT)
    price = Column(DECIMAL)

    address = Column(TEXT)
    lat = Column(FLOAT)
    lng = Column(FLOAT)
