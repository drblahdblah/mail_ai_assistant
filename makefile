.PHONY: ingest index tone run ui clean

# Ingest emails from macOS Mail.app into JSON
ingest:
	@echo "📥 Ingesting emails from macOS Mail..."
	python scripts/ingest_emails.py

# Build semantic vector index from parsed emails
index:
	@echo "🧠 Building vector index..."
	python backend/index_builder.py

# Generate tone embeddings from your own replies
tone:
	@echo "🎙️ Embedding tone vectors..."
	python backend/tone_adapter.py

# Run full decision + draft pipeline on a few recent emails
run:
	@echo "🤖 Running full pipeline on emails..."
	PYTHONPATH=. python scripts/run_local_app.py

# Launch Gradio frontend UI
ui:
	@echo "🖥️  Launching Gradio UI..."
	PYTHONPATH=. python frontend/ui.py

# Clean all generated data (careful!)
clean:
	@echo "🧹 Cleaning all generated data..."
	rm -rf data/vector_index data/user_embeddings data/drafts
