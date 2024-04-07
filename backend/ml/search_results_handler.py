from typing import Any

from langchain.prompts import PromptTemplate, load_prompt
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from schemas.event import Event, EventType

system_prompt_template = load_prompt("ml/prompts/search_system.yaml")
next_system_prompt_template = load_prompt("ml/prompts/search_qna_system.yaml")

def generate_metadata_string(event_type: EventType, metadata: dict[str, Any]) -> str:
    if event_type == EventType.RESTAURANT:
        price_info = (
            f"Средний чек в ресторане составляет {metadata['price']}"
            if "price" in metadata and metadata["price"]
            else ""
        )
        kitchen_type_info = (
            f'В ресторане представлены следующие кухни: {"- ".join(metadata["restaurant_type"])}'
            if "restaurant_type" in metadata and metadata["restaurant_type"]
            else ""
        )
        location_info = (
            f'Ресторан находится по адресу: {metadata["location"]}'
            if "location" in metadata and metadata["location"]
            else ""
        )
        metadata_info = "\n".join(
            [price_info, kitchen_type_info, location_info]
        ).strip()
    elif event_type == EventType.EVENT:
        price_info = ""
        if "price" in metadata and metadata["price"]:
            if metadata["price"] > 0:
                price_info = f"Цена посещения составляет {metadata['price']}"
            else:
                price_info = "Посещение данного мероприятия полностью бесплатно"
        metadata_info = "\n".join([price_info]).strip()
    else:
        raise ValueError("invalid event type")
    return metadata_info


def generate_messages_for_chat(user_input: str, event: Event) -> list[BaseMessage]:
    metadata_string = generate_metadata_string(event.type_, event.export_metadata())
    system_message = system_prompt_template.format(
        user_input_text=user_input,
        event_name=event.name,
        event_description=event.description,
        event_metadata=metadata_string,
    )
    messages = [SystemMessage(content=system_message)]
    return messages

def generate_messages_for_continous_chat(event: Event) -> list[BaseMessage]:
    metadata_string = generate_metadata_string(event.type_, event.export_metadata())
    system_message = next_system_prompt_template.format(
        event_name=event.name,
        event_description=event.description,
        event_metadata=metadata_string,
    )
    messages = [SystemMessage(content=system_message)]
    return messages