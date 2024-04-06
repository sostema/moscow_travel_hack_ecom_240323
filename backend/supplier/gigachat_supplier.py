import re
from dataclasses import dataclass

import ujson
from langchain.chat_models.gigachat import GigaChat
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from shared.settings import app_settings

message_history = list[AIMessage | HumanMessage | SystemMessage]


@dataclass
class GigachatSupplier:
    def __post_init__(self) -> None:
        self._system_prompt = "Ты умный ассистент, помогающий людям провести время, подбирая лучшие события чтобы посетить их."
        self.chat = GigaChat(
            credentials=app_settings.gigachat_auth_key,
            verify_ssl_certs=False,
        )

    def dump_message_history(self, history: message_history) -> str:
        jsonable = []
        for message in history:
            jsonable.append({"content": message.content, "type": message.type})
        return ujson.dumps(jsonable, ensure_ascii=False)

    def load_message_history(self, jsonable: str) -> message_history:
        history = []
        for message in ujson.loads(jsonable):
            if message["type"] == "human":
                history.append(HumanMessage(content=message["content"]))
            elif message["type"] == "system":
                history.append(SystemMessage(content=message["content"]))
            else:
                history.append(AIMessage(content=message["content"]))

        return history

    def message(
        self, prompt: str, history: message_history | None = None
    ) -> message_history:
        if history is None:
            history = [SystemMessage(content=self._system_prompt)]

        history.append(HumanMessage(content=prompt))
        res = self.chat(history)
        history.append(AIMessage(content=res.content))

        return history

    def translate_to_english(self, prompt: str) -> str:
        is_eng = re.match(r"^[a-zA-Z0-9\W]*$", prompt)
        if not is_eng:
            messages = [
                HumanMessage(
                    content=f"Переведи фразу «{prompt}» на английский. В ответе должна быть только переведенная фраза. "
                    "Например на запрос «Переведи фразу «солнце»», ответ будет: «Sun»."
                    "Если фраза уже на английском, то верни эту фразу. "
                    "Например на запрос «Переведи фразу «Sun»», ответ будет: «Sun»."
                )
            ]
            prompt = str(self.chat(messages).content)

        is_broken = re.match(r'^"[\'a-zA-Z0-9\W]*".*"[\'a-zA-Z0-9\W]*".$', prompt)
        if is_broken:
            m = re.search(r'"[a-zA-Z0-9\W]*".$', prompt)
            prompt = str(m.group(0))

        return prompt.strip('"')
