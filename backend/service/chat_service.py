from dataclasses import dataclass

from ml import classify_event_type
from ml.retrieval_manager import RetrievalManager
from repository.redis_repository import RedisRepository
from schemas.message import BaseMessage, Message, Messages, MessageType
from shared.base import logger
from shared.ulid import ulid_as_uuid
from supplier.gigachat_supplier import GigachatSupplier


class HistoryNotFound(Exception):
    ...


@dataclass
class ChatService:
    gigachat_supplier: GigachatSupplier
    redis_repository: RedisRepository
    retrieval_manager: RetrievalManager

    def search(self, query: str) -> Message:
        message = classify_event_type.generate_messages_for_chat(query)
        resp = self.gigachat_supplier.chat(message)
        event_type = classify_event_type.parse_response_for_types(resp.content)

        doc = self.retrieval_manager.retrieve_most_relevant_document(event_type, query)
        print(doc.metadata)

        return Message(text="AAAA", type_=MessageType.HUMAN)

    def _get_path_messages(self, history_id: str) -> str:
        return f"chat::{history_id}"

    def get_history(self, history_id: str) -> Messages:
        history_raw = self.redis_repository.rget(self._get_path_messages(history_id))
        if history_raw is None:
            raise HistoryNotFound()

        history = Messages.parse_raw(history_raw.decode())
        filtered_messages = []
        for message in history.messages:
            if message.type_ == MessageType.SYSTEM:
                continue
            filtered_messages.append(message)

        history.messages = filtered_messages
        return history

    def dump_history(self, history_id: str, history: Messages) -> None:
        self.redis_repository.rset(self._get_path_messages(history_id), history.json())

    def get_all_histories(self) -> list[str]:
        histories = self.redis_repository.keys(self._get_path_messages("*"))

        return [history_id.decode().split("::")[1] for history_id in histories]

    def send_message(self, message: str, history_id: str | None) -> tuple[Message, str]:
        logger.debug("Sending message in history_id: {}", history_id)

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
            history = Messages.parse_raw(history_raw.decode())

        history = self.gigachat_supplier.message(message, history=history)
        logger.info("Chat history: {}, history_id: {}", history, history_id)

        self.dump_history(history_id, history)

        return history.messages[-1], history_id
