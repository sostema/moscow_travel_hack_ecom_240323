from typing import Any

from langchain_core.messages.base import BaseMessage
from schemas.base import CamelizedBaseModel
from schemas.event import Event


class Message(CamelizedBaseModel):
    chain_message: Any

    event: Event | None = None
    description: str | None = None

    @classmethod
    def from_chain_message(cls, message: BaseMessage) -> "Message":
        return cls(chain_message=message)


class Messages(CamelizedBaseModel):
    messages: list[Message]

    def extract_chain_message(self) -> list[BaseMessage]:
        return [message.chain_message for message in self.messages]
