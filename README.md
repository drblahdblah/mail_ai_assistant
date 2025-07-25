# ✉️ Local AI Email Assistant (Private, Secure, Local-Only)

This project is a fully local AI-powered email assistant that:

- 🧠 Recommends whether you need to reply to an email
- 💬 Suggests reply drafts using your personal tone and past replies
- 🔍 Retrieves relevant past emails for better context (RAG)
- 🔒 Runs **entirely locally** using [Ollama](https://ollama.com), [LangChain](https://www.langchain.com/), and [LlamaIndex](https://www.llamaindex.ai/)

---

## 📦 Features

| Feature                        | Technology             |
|-------------------------------|------------------------|
| Email ingestion (Mail.app)    | Python email parser    |
| Vector search (RAG)           | LlamaIndex + FAISS     |
| Local LLM inference           | Ollama (e.g., LLaMA3)  |
| Tone modeling                 | HuggingFace Embeddings |
| Agentic decision-making       | LangChain / custom agent |
| Interactive frontend          | Gradio UI              |

---

## 🚀 Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/yourname/local-email-assistant.git
cd local-email-assistant
pip install -r requirements.txt
````

Make sure you have [Ollama](https://ollama.com/) installed and running.

### 2. Run the Pipeline

```bash
make ingest     # Ingests emails from macOS Mail.app (Maildir)
make index      # Builds vector search index
make tone       # Embeds your personal tone from past replies
make run        # Runs the AI decision + drafting pipeline
make ui         # Launches the Gradio UI
```

### 2. Using Pyproject.toml and setup.pt

🧑‍💻 How to install & develop
# From the root directory (where setup.py & pyproject.toml live)
```bash pip install -e . ```

You can then run:
```bash 
email-ai-ingest
email-ai-run
email-ai-ui
```
---

## 🧰 Project Structure

```bash
email_ai_assistant/
├── backend/              # Core modules: parsing, agents, drafting, tone
├── data/                 # Raw emails, vector index, tone embeddings
├── frontend/             # Gradio UI
├── models/               # Ollama inference wrapper
├── scripts/              # Pipelines and batch processing
├── tests/                # Test harnesses
├── Makefile              # Dev tasks runner
├── requirements.txt
└── README.md
```

---

## 💡 Examples

### Incoming Email:

```
Subject: Q3 Revenue Forecast

Hi, just wondering if you had time to look at the Q3 revenue forecast. We’d like to wrap it by Friday.
```

### Agent Decision:

```
[REPLY]
Reason: This email is requesting timely input before a deadline.
```

### Suggested Draft:

```
Thanks for the reminder! Yes, I’m reviewing it today and will share comments by tomorrow at the latest.
```

---

## 🔐 Security

All data is stored and processed **locally**:

* No API keys or external services
* All model inference is done via [Ollama](https://ollama.com/)
* Embeddings, vector DB, and drafts remain on your device

---

## 🧪 Development Tips

* Use `make ingest index run` to refresh your environment quickly.
* You can edit prompt logic in:

  * `agent_decider.py`
  * `draft_generator.py`
  * `tone_adapter.py`

---

## 📌 TODO / Future Improvements

* [ ] Add Gmail IMAP support
* [ ] MCTS planner for more advanced agent decisions
* [ ] Archive / send integration
* [ ] Summarize email threads before replying
* [ ] Web or desktop app (Electron)

---

## 🧑‍💻 Author

Built by [Your Name](https://github.com/yourname).
Inspired by the idea of **local-first AI** tools that prioritize privacy and productivity.

---

## 📝 License

MIT License. Use at your own risk.

```

[![codecov](https://codecov.io/gh/yourusername/yourrepo/branch/main/graph/badge.svg?token=YOURTOKEN)](https://codecov.io/gh/yourusername/yourrepo)
