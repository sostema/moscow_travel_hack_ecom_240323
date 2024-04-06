from dataclasses import dataclass

from repository.redis_repository import RedisRepository
from shared.base import logger
from shared.ulid import ulid_as_uuid
from supplier.gigachat_supplier import GigachatSupplier


class HistoryNotFound(Exception):
    ...


@dataclass
class ChatService:
    gigachat_supplier: GigachatSupplier
    redis_repository: RedisRepository

    def send_message(self, message: str, history_id: str | None) -> tuple[str, str]:
        if history_id is None:
            history_id = str(ulid_as_uuid())
            history = None
        else:
            history_raw = self.redis_repository.rget(history_id)
            if history_raw is None:
                raise HistoryNotFound()
            history = self.gigachat_supplier.load_message_history(history_raw.decode())

        history = self.gigachat_supplier.message(message, history=history)
        logger.info("Chat history: {}, history_id: {}", history, history_id)

        history_dumped = self.gigachat_supplier.dump_message_history(history)
        self.redis_repository.rset(history_id, history_dumped)

        return str(history[-1].content), history_id
