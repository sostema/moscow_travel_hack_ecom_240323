import re
from typing import Any, Optional

from langchain.prompts import PromptTemplate, load_prompt
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

system_prompt_template = load_prompt(
    "src/mthe_ml/prompts/zeroshot_classification_system.yaml"
)


def generate_messages_for_chat(
    text: str, categories: Optional[list[str]]
) -> list[BaseMessage]:
    if not categories:
        categories = ["Ресторан"]
    system_message = system_prompt_template.format(
        text=text, categories=", ".join(categories)
    )
    messages = [SystemMessage(content=system_message)]
    return messages


def parse_response_for_types(message: str, categories: Optional[list[str]]) -> str:
    if not categories:
        categories = ["Ресторан"]
    for cat in categories:
        if cat.lower() in message.lower():
            return cat
    return "Другое"
