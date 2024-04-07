import random
from dataclasses import dataclass

from langchain.schema import AIMessage, HumanMessage
from ml import classify_event_type, search_results_handler
from ml.retrieval_manager import RetrievalManager
from repository.pg_repository import PgRepository
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
    pg_repository: PgRepository

    def __post_init__(self) -> None:
        self.string_header_what_do_you_think = [
            "Что скажете по поводу этого мероприятия?",
            "Смотрите, что я нашла",
            "А как вам такое?",
        ]

    def search_continue(self, query: str, history_id: str) -> Message:
        history = self.load_history(history_id)
        if history.messages[0].event is None:
            return Message(
                text='Упс, что-то пошло не так:(\nПопробуй отправить слово "стоп" и спросить меня снова',
                type=MessageType.AI,
            )

        messages = search_results_handler.generate_messages_for_continous_chat(
            history.messages[0].event,
        )
        messages.append(HumanMessage(content=query))
        resp = self.gigachat_supplier.chat.invoke(messages)
        messages.append(resp)

        domain_messages = Messages.from_chain_message(messages=messages)
        domain_messages.messages[0].event = history.messages[0].event
        self.dump_history(history_id, domain_messages)

        return domain_messages.messages[-1]

    def search(self, query: str) -> tuple[Message, str]:
        message = classify_event_type.generate_messages_for_chat(query)
        resp = self.gigachat_supplier.chat.invoke(message)
        event_type = classify_event_type.parse_response_for_types(resp.content)

        doc = self.retrieval_manager.retrieve_most_relevant_document(event_type, query)

        event = self.pg_repository.get_event(id_=doc.metadata["id"])

        message = search_results_handler.generate_messages_for_chat(
            user_input=query, event=event
        )
        resp = self.gigachat_supplier.chat.invoke(message)

        domain_message = Message(
            text=random.choice(self.string_header_what_do_you_think),
            description=resp.content,
            type=MessageType.AI,
            event=event,
        )
        history_id = str(ulid_as_uuid())
        self.dump_history(history_id, Messages(messages=[domain_message]))

        return domain_message, history_id

    def _get_path_messages(self, history_id: str) -> str:
        return f"chat::{history_id}"

    def get_history(self, history_id: str, remove_system: bool) -> Messages:
        history = self.load_history(history_id)
        if not remove_system:
            return history

        filtered_messages = []
        for message in history.messages:
            if message.type_ == MessageType.SYSTEM:
                continue
            filtered_messages.append(message)

        history.messages = filtered_messages
        return history

    def dump_history(self, history_id: str, history: Messages) -> None:
        self.redis_repository.rset(self._get_path_messages(history_id), history.json())
        logger.info("history dumped: {}", history.jsonable_encoder())

    def get_all_histories(self) -> list[str]:
        histories = self.redis_repository.keys(self._get_path_messages("*"))

        return [history_id.decode().split("::")[1] for history_id in histories]

    def load_history(self, history_id: str) -> Messages:
        history_raw = self.redis_repository.rget(self._get_path_messages(history_id))
        if history_raw is None:
            raise HistoryNotFound()
        history = Messages.parse_raw(history_raw.decode())

        logger.info("history loaded: {}", history.jsonable_encoder())
        return history

    def send_message(self, message: str, history_id: str | None) -> tuple[Message, str]:
        if history_id is None:
            history_id = str(ulid_as_uuid())
            history = None
        else:
            # TODO posible racecond, rewrite using pessimistic lock
            history = self.load_history(history_id)

        history = self.gigachat_supplier.message(message, history=history)
        logger.info("Chat history: {}, history_id: {}", history, history_id)

        self.dump_history(history_id, history)

        return history.messages[-1], history_id
