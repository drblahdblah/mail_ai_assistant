"""
Entrypoint to run everything locally
"""
from pathlib import Path
import json
from backend.agent_decider import decide_reply_action
from backend.draft_generator import generate_draft_reply
from backend.tone_adapter import build_tone_prompt, retrieve_similar_tone_examples

RAW_EMAIL_DIR = Path("data/raw_emails")
OUTPUT_DIR = Path("data/drafts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def process_email(email_path: Path):
    with open(email_path, 'r') as f:
        email_data = json.load(f)

    email_text = f"From: {email_data.get('from')}\nSubject: {email_data.get('subject')}\n\n{email_data.get('body')}"
    subject = email_data.get('subject') or "[No Subject]"
    print(f"\n🔍 Processing: {subject[:50]}...")
    
    # Step 1: Decide whether to reply
    decision = decide_reply_action(email_text)
    print(f"🤖 Decision: {decision['action']} | Reason: {decision['reason']}")

    if decision['action'] == "REPLY":
        # Step 2: Generate reply with context + tone
        draft_reply = generate_draft_reply(email_text)
        # Or: build tone prompt directly:
        # tone_prompt = build_tone_prompt(email_text)
        # draft_reply = query_ollama(tone_prompt)

        # Step 3: Save draft
        draft_file = OUTPUT_DIR / (email_path.stem + "_reply.txt")
        with open(draft_file, 'w', encoding='utf-8') as f:
            f.write(draft_reply)
        print(f"💌 Draft saved: {draft_file.name}")
    else:
        print("📥 No reply generated.")


def main(limit=None):
    files = sorted(RAW_EMAIL_DIR.glob("*.json"))[:limit]
    print(f"📬 Found {len(files)} emails.")

    for email_path in files:
        process_email(email_path)


if __name__ == "__main__":
    # Change the number to limit emails processed during testing
    main(limit=5)
