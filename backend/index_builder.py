import os
import json
from pathlib import Path
import faiss

from llama_index.core import VectorStoreIndex, Document
from llama_index.core.storage import StorageContext
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings

# --- Configuration ---
RAW_EMAIL_DIR = Path('data/raw_emails')
INDEX_DIR = Path('data/vector_index')
INDEX_DIR.mkdir(parents=True, exist_ok=True)

# --- Embedding Setup (offline) ---
EMBEDDING_MODEL = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.embed_model = EMBEDDING_MODEL  # MUST be set early


def load_emails_as_documents():
    documents = []
    for file_path in RAW_EMAIL_DIR.glob('*.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            email = json.load(f)
            text = f"From: {email.get('from')}\nTo: {email.get('to')}\nSubject: {email.get('subject')}\nDate: {email.get('date')}\n\n{email.get('body')}"
            metadata = {
                'from': email.get('from'),
                'to': email.get('to'),
                'subject': email.get('subject'),
                'date': email.get('date'),
            }
            documents.append(Document(text=text, metadata=metadata))
    return documents


def build_and_save_index(documents):
    # Convert to nodes
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)

    # Determine embedding dimension
    dim = len(EMBEDDING_MODEL.get_text_embedding("dummy"))

    # Build FAISS index
    faiss_index = faiss.IndexFlatL2(dim)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Build index
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    index.storage_context.persist(persist_dir=str(INDEX_DIR))
    print(f"✅ Index saved to {INDEX_DIR}")


def main():
    print("📥 Loading parsed emails...")
    docs = load_emails_as_documents()
    print(f"📄 Loaded {len(docs)} documents")

    print("⚙️ Building and saving vector index...")
    build_and_save_index(docs)


if __name__ == "__main__":
    main()
