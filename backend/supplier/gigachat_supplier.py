import re
from dataclasses import dataclass

import redis
from langchain.cache import RedisCache
from langchain.chat_models.gigachat import GigaChat
from langchain.globals import set_llm_cache
from langchain.schema import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from repository.redis_repository import RedisRepository
from shared.settings import app_settings


@dataclass
class GigachatSupplier:
    redis_repository: RedisRepository

    def __post_init__(self) -> None:
        self.chat = GigaChat(
            credentials=app_settings.gigachat_auth_key,
            verify_ssl_certs=False,
        )
        set_llm_cache(RedisCache(self.redis_repository.r))

    def single_message(self, prompt: str) -> str:
        messages = [HumanMessage(content=prompt)]
        res = self.chat(messages)

        return str(res.content)

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
