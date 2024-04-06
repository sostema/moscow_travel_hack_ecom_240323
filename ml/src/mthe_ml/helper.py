from langchain.chains.query_constructor.base import AttributeInfo
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.embeddings import Embeddings

from .configs import pgvector_connection_string


def get_pgvector_store(embeddings_model: Embeddings, collection_name: str):
    store = PGVector(
        collection_name=collection_name,
        connection_string=pgvector_connection_string,
        embedding_function=embeddings_model,
    )
    return store
