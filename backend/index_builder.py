"""
 Indexes emails with LlamaIndex
"""
import os
import json
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.schema import Document
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import ServiceContext, set_global_service_context
from llama_index.embeddings.openai import OpenAIEmbedding  # Replace if using local embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# --- Configuration ---
RAW_EMAIL_DIR = Path('data/raw_emails')
INDEX_DIR = Path('data/vector_index')
INDEX_DIR.mkdir(parents=True, exist_ok=True)

# Choose an embedding model (Ollama-compatible via HuggingFace or sentence-transformers)
EMBEDDING_MODEL = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


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
    # Setup embedding + service context
    service_context = ServiceContext.from_defaults(embed_model=EMBEDDING_MODEL)
    set_global_service_context(service_context)

    # Parse text into nodes (optional chunking)
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents(documents)

    # Create and save FAISS index
    vector_store = FaissVectorStore()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    # Persist the index
    index.storage_context.persist(persist_dir=str(INDEX_DIR))
    print(f'Index saved to {INDEX_DIR}')


def main():
    print('Loading parsed emails...')
    docs = load_emails_as_documents()
    print(f'Loaded {len(docs)} documents.')
    
    print('Building and saving vector index...')
    build_and_save_index(docs)


if __name__ == '__main__':
    main()
