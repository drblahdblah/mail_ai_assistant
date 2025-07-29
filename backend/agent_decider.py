"""
Agent Q + MCTS based logic to decide if reply is needed
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"  # or mistral, phi, etc.

DECISION_PROMPT_TEMPLATE = """
You are an assistant helping a user triage their emails. Based on the content of the email below, determine whether the user should reply, archive, or reply later.

Email:
---
{email}
---

Respond with one of the following categories ONLY: [REPLY], [ARCHIVE], [REPLY_LATER]
Also provide a one-sentence justification after the category.
Format:
CATEGORY: [REPLY]
REASON: Because it requires a timely response about an upcoming deadline.
"""


def build_decision_prompt(email_text: str) -> str:
    return DECISION_PROMPT_TEMPLATE.format(email=email_text)


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


def decide_reply_action(email_text: str) -> dict:
    prompt = build_decision_prompt(email_text)
    result = query_ollama(prompt)

    # Parse response
    decision = {}
    if "CATEGORY:" in result:
        lines = result.splitlines()
        for line in lines:
            if line.startswith("CATEGORY:"):
                decision['action'] = line.split(":", 1)[1].strip().strip("[]")
            elif line.startswith("REASON:"):
                decision['reason'] = line.split(":", 1)[1].strip()
    else:
        # fallback
        decision = {
            "action": "REPLY_LATER",
            "reason": "Could not confidently classify email, defaulting to REPLY_LATER."
        }
    return decision


# 🧪 Example usage
if __name__ == '__main__':
    example_email = """
Hey, just wanted to follow up on the invoice from last week. Let me know if you need me to resend it.
Best,  
Sam
"""
    decision = decide_reply_action(example_email)
    print(f"Decision: {decision['action']}\nReason: {decision['reason']}")
