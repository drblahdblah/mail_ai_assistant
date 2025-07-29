"""
Tone modeling and personalization
"""

import os
import json
from pathlib import Path
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import Document
from sentence_transformers.util import cos_sim

# --- Config ---
EMBED_MODEL = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
TONE_VECTOR_STORE = Path('data/user_embeddings/replies.json')


def load_past_replies_for_embedding() -> list[dict]:
    replies = []
    raw_dir = Path('data/raw_emails')

    for file in raw_dir.glob('*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            try:
                email = json.load(f)
            except json.JSONDecodeError:
                continue

            sender = email.get('from') or ''  # ensure it's a string, even if missing

            if (
                sender.startswith('me@') or
                'davidjones42@icloud.com' in sender or
                'drblahdblah@gmail.com' in sender
            ):
                body = email.get('body') or ''
                if body.strip():  # only add non-empty replies
                    replies.append({
                        'text': body,
                        'metadata': {
                            'date': email.get('date'),
                            'subject': email.get('subject'),
                        }
                    })

    return replies



def embed_and_save_tone_vectors():
    os.makedirs(TONE_VECTOR_STORE.parent, exist_ok=True)
    replies = load_past_replies_for_embedding()
    vectors = []
    for r in replies:
        vec = EMBED_MODEL.get_text_embedding(r['text'])
        vectors.append({
            'embedding': vec,
            'text': r['text'],
            'metadata': r['metadata']
        })
    with open(TONE_VECTOR_STORE, 'w') as f:
        json.dump(vectors, f)
    print(f"Saved {len(vectors)} embedded replies.")


def retrieve_similar_tone_examples(input_text: str, top_k=3):
    if not TONE_VECTOR_STORE.exists():
        raise FileNotFoundError('Tone vector store missing. Run embed_and_save_tone_vectors() first.')

    with open(TONE_VECTOR_STORE, 'r') as f:
        stored = json.load(f)

    query_vec = EMBED_MODEL.get_text_embedding(input_text)

    scored = []
    for entry in stored:
        score = cos_sim(query_vec, entry['embedding'])[0][0].item()
        scored.append((score, entry))

    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:top_k]

    return [e['text'] for _, e in top]


def build_tone_prompt(email_text: str) -> str:
    similar_examples = retrieve_similar_tone_examples(email_text)
    tone_injection = '\n\n'.join(f"- {e}" for e in similar_examples)

    return f"""
You are writing a reply that matches the user's tone and style. Here are previous examples of how they typically write:

{tone_injection}

Now generate a reply to this new email, using a similar tone:
---
{email_text}
"""


# 🧪 Example usage
if __name__ == '__main__':
    embed_and_save_tone_vectors()

    new_email = """Hi, are you still able to present at the Q3 planning session next Tuesday? Let me know so I can update the calendar."""
    prompt = build_tone_prompt(new_email)
    print('--- Injected Prompt ---\n', prompt)
