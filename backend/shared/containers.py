from dataclasses import dataclass

from repository.pg_repository import PgRepository
from repository.redis_repository import RedisRepository
from service.chat_service import ChatService
from service.heath_service import HeathService
from supplier.gigachat_supplier import GigachatSupplier


@dataclass
class Container:
    heath_service: HeathService
    redis_repository: RedisRepository
    chat_service: ChatService


def init_combat_container() -> Container:
    redis_repository = RedisRepository()
    pg_repository = PgRepository()
    heath_service = HeathService(
        redis_repository=redis_repository, pg_repository=pg_repository
    )

    gigachat_supplier = GigachatSupplier()
    chat_service = ChatService(
        gigachat_supplier=gigachat_supplier, redis_repository=redis_repository
    )

    return Container(
        heath_service=heath_service,
        redis_repository=redis_repository,
        chat_service=chat_service,
    )
