from dataclasses import dataclass

from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage
from schemas.message import Message, Messages
from shared.settings import app_settings


@dataclass
class GigachatSupplier:
    def __post_init__(self) -> None:
        self._system_prompt = "Ты умный ассистент, помогающий людям провести время, подбирая лучшие события чтобы посетить их."
        self.chat = GigaChat(
            credentials=app_settings.gigachat_auth_key,
            verify_ssl_certs=False,
        )

    def message(self, prompt: str, history: Messages | None = None) -> Messages:
        if history is None:
            history = Messages(
                messages=[
                    Message.from_chain_message(
                        SystemMessage(content=self._system_prompt)
                    )
                ]
            )

        history.messages.append(
            Message.from_chain_message(HumanMessage(content=prompt))
        )
        res = self.chat(history.extract_chain_message())
        history.messages.append(Message.from_chain_message(res))

        return history
