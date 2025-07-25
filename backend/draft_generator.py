"""
 Prompt builder + Ollama inference wrapper
 """

import requests
from llama_index.core import load_index_from_storage
from llama_index.core.storage import StorageContext

from backend.tone_adapter import build_tone_prompt

# --- Config ---
OLLAMA_MODEL = 'llama3'  # or 'mistral', 'phi', etc.
OLLAMA_URL = 'http://localhost:11434/api/generate'
INDEX_PATH = 'data/vector_index'


def load_query_engine():
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_PATH)
    index = load_index_from_storage(storage_context)
    return index.as_query_engine(similarity_top_k=4)


def build_prompt(new_email: str, retrieved_context: str) -> str:
    return f"""
You are an AI assistant that drafts email replies in the user's style.
Here is a new email that the user received:

--- Incoming Email ---
{new_email}

--- Relevant Past Conversations ---
{retrieved_context}

Write a thoughtful, context-aware reply that matches the user's previous tone and style.
Keep the response professional but friendly. Begin directly with the user's reply (no \"Dear...\" or \"Response:\").
"""


def query_ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code != 200:
        raise RuntimeError(f"Ollama error: {response.text}")
    return response.json()['response'].strip()


def generate_draft_reply(new_email_text: str, use_tone=False) -> str:

    query_engine = load_query_engine()
    rag_response = query_engine.query(new_email_text)

    if use_tone:
        prompt = build_prompt(new_email_text, str(rag_response))
    else:
        prompt = build_tone_prompt(email_text=new_email_text)
    return query_ollama(prompt)


# 🧪 Example usage
if __name__ == '__main__':
    sample_incoming = """
Hi, just wondering if you had time to look at the Q3 revenue forecast. We’d like to wrap it by Friday if possible.
Best,
Elena
"""
    reply = generate_draft_reply(sample_incoming)
    print(f'--- Draft Reply ---\n{reply}')
