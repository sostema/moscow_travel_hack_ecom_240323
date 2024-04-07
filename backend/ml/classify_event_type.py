from langchain.prompts import PromptTemplate, load_prompt
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from schemas.event import EventType

system_prompt_template = load_prompt("ml/prompts/zeroshot_classification_system.yaml")

ru_to_event_type: dict[str, EventType] = {
    "Ресторан": EventType.RESTAURANT,
    "Другое": EventType.EVENT,
}


def generate_messages_for_chat(text: str) -> list[BaseMessage]:
    categories = ["Ресторан"]
    system_message = system_prompt_template.format(
        text=text, categories=", ".join(categories)
    )
    messages = [SystemMessage(content=system_message)]
    return messages


def parse_response_for_types(message: str) -> str:
    categories = ["Ресторан"]
    for cat in categories:
        if cat.lower() in message.lower():
            return ru_to_event_type[cat]

    return ru_to_event_type["Другое"]
