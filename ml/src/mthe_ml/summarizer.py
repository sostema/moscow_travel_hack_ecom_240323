from gigachat import GigaChat
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import load_prompt
from langchain.text_splitter import RecursiveCharacterTextSplitter


def summarize(llm: GigaChat, text_list: list[str]) -> str:
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=256, chunk_overlap=64
    )
    document_splits = text_splitter.create_documents(text_list)
    map_prompt = load_prompt("src/mthe_ml/prompts/summarize_map_system.yaml")
    combine_prompt = load_prompt("src/mthe_ml/prompts/summarize_combine_system.yaml")
    summarize_chain = load_summarize_chain(
        llm,
        map_prompt=map_prompt,
        combine_prompt=combine_prompt,
        chain_type="map_reduce",
    )
    summarized_text = summarize_chain(document_splits)
    return summarized_text
