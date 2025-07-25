"""
Gradio/Streamlit interface
"""
import gradio as gr
import json
from pathlib import Path
from backend.agent_decider import decide_reply_action
from backend.draft_generator import generate_draft_reply

RAW_EMAIL_DIR = Path("data/raw_emails")


def load_email_options():
    files = sorted(RAW_EMAIL_DIR.glob("*.json"))
    return [f.name for f in files]


def load_email(file_name):
    file_path = RAW_EMAIL_DIR / file_name
    with open(file_path, 'r') as f:
        email = json.load(f)
    preview = f"From: {email.get('from')}\nSubject: {email.get('subject')}\n\n{email.get('body')}"
    return preview


def run_pipeline(file_name):
    file_path = RAW_EMAIL_DIR / file_name
    with open(file_path, 'r') as f:
        email_data = json.load(f)

    email_text = f"From: {email_data.get('from')}\nSubject: {email_data.get('subject')}\n\n{email_data.get('body')}"
    decision = decide_reply_action(email_text)

    if decision["action"] == "REPLY":
        draft = generate_draft_reply(email_text)
    else:
        draft = f"[{decision['action']}] — No draft needed.\nReason: {decision['reason']}"

    return decision['action'], decision['reason'], draft


with gr.Blocks(title="Local Email Assistant") as demo:
    gr.Markdown("# ✉️ Local Email AI Assistant")

    with gr.Row():
        email_selector = gr.Dropdown(choices=load_email_options(), label="Choose an Email")
        load_button = gr.Button("Load Email")

    email_preview = gr.Textbox(label="Email Content", lines=10)
    
    with gr.Row():
        decision_output = gr.Textbox(label="Decision (Reply / Archive / Later)", interactive=False)
        reason_output = gr.Textbox(label="Reason", interactive=False)

    with gr.Row():
        draft_output = gr.Textbox(label="Suggested Reply Draft", lines=10)
    
    run_button = gr.Button("Run AI Pipeline")

    # --- Logic binding ---
    load_button.click(fn=load_email, inputs=email_selector, outputs=email_preview)
    run_button.click(fn=run_pipeline, inputs=email_selector, outputs=[decision_output, reason_output, draft_output])


if __name__ == '__main__':
    demo.launch()
