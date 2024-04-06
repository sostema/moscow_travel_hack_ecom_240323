from enum import StrEnum
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages.base import BaseMessage
from schemas.base import CamelizedBaseModel
from schemas.event import Event


class MessageType(StrEnum):
    AI = "ai"
    SYSTEM = "system"
    HUMAN = "human"


class Message(CamelizedBaseModel):
    text: str
    type_: MessageType

    event: Event | None = None
    description: str | None = None

    @classmethod
    def from_chain_message(cls, message: BaseMessage) -> "Message":
        return cls(text=message.content, type_=MessageType(message.type))

    def to_chain_message(self) -> BaseMessage:
        if self.type_ == MessageType.AI:
            return AIMessage(content=self.text)
        if self.type_ == MessageType.SYSTEM:
            return SystemMessage(content=self.text)
        if self.type_ == MessageType.HUMAN:
            return HumanMessage(content=self.text)
        raise ValueError("unknown chain message type...")


class Messages(CamelizedBaseModel):
    messages: list[Message]

    def extract_chain_message(self) -> list[BaseMessage]:
        return [message.to_chain_message() for message in self.messages]

    @classmethod
    def from_chain_message(cls, messages: list[BaseMessage]) -> "Messages":
        return cls(
            messages=[Message.from_chain_message(message) for message in messages]
        )
