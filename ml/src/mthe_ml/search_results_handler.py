from typing import Any

from langchain.prompts import PromptTemplate, load_prompt
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

system_prompt_template = load_prompt("./prompts/search_system.yaml")


def generate_metadata_string(event_type: str, metadata: dict[str, Any]) -> str:
    if event_type == "restaurant":
        price_info = (
            f"Средний чек в ресторане составляет {metadata['price']}"
            if "price" in metadata
            else ""
        )
        kitchen_type_info = (
            f'В ресторане представлены следующие кухни: {"- ".join(metadata['kitchen_type'])}'
            if "kitchen_type" in metadata
            else ""
        )
        location_info = (
            f'Ресторан находится по адресу: {metadata['location']}'
            if "location" in metadata
            else ""
        )
        metadata_info = "\n".join(
            [price_info, kitchen_type_info, location_info]
        ).strip()
    elif event_type == "event":
        price_info = ""
        if "price" in metadata:
            if metadata["price"] > 0:
                price_info = f"Цена посещения составляет {metadata['price']}"
            else:
                price_info = "Посещение данного мероприятия полностью бесплатно"
        metadata_info = "\n".join([price_info]).strip()
    else:
        raise ValueError
    return metadata_info


def get_event_from_db(event_id: int) -> tuple[str, str, str, dict[str, Any]]:
    # mockup
    return "event_name", "event_text", "event", {"price": 120}


def generate_messages_for_chat(event_id: int) -> list[BaseMessage]:
    event_name, event_text, event_type, event_metadata = get_event_from_db(id=event_id)
    metadata_string = generate_metadata_string(event_type, event_metadata)
    system_message = system_prompt_template.format(
        event_name=event_name,
        event_description=event_text,
        event_metadata=metadata_string,
    )
    messages = [SystemMessage(content=system_message)]
    return messages
