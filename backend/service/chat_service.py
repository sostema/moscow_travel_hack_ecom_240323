from dataclasses import dataclass

from pydantic import TypeAdapter
from repository.redis_repository import RedisRepository
from schemas.base import CamelizedBaseModel
from shared.base import logger
from shared.ulid import ulid_as_uuid
from supplier.gigachat_supplier import GigachatSupplier


class HistoryNotFound(Exception):
    ...


class Message(CamelizedBaseModel):
    content: str
    type: str


@dataclass
class ChatService:
    gigachat_supplier: GigachatSupplier
    redis_repository: RedisRepository

    def _get_path_messages(self, history_id: str) -> str:
        return f"chat::{history_id}"

    def get_history(self, history_id: str) -> list[Message]:
        history_raw = self.redis_repository.rget(self._get_path_messages(history_id))

        messages = TypeAdapter(list[Message]).validate_json(history_raw)
        filtered_messages = []
        for message in messages:
            if message.type == "system":
                continue
            filtered_messages.append(message)

        return filtered_messages

    def get_all_histories(self) -> list[str]:
        histories = self.redis_repository.keys(self._get_path_messages("*"))

        return [history_id.decode().split("::")[1] for history_id in histories]

    def send_message(self, message: str, history_id: str | None) -> tuple[str, str]:
        if history_id is None:
            history_id = str(ulid_as_uuid())
            history = None
        else:
            # TODO posible racecond, rewrite using pessimistic lock
            history_raw = self.redis_repository.rget(
                self._get_path_messages(history_id)
            )
            if history_raw is None:
                raise HistoryNotFound()
            history = self.gigachat_supplier.load_message_history(history_raw.decode())

        history = self.gigachat_supplier.message(message, history=history)
        logger.info("Chat history: {}, history_id: {}", history, history_id)

        history_dumped = self.gigachat_supplier.dump_message_history(history)
        self.redis_repository.rset(self._get_path_messages(history_id), history_dumped)

        return str(history[-1].content), history_id
