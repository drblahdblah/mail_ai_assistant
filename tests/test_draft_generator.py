import pytest
from backend.draft_generator import generate_draft_reply

def test_generate_draft_reply_returns_string(monkeypatch):
    sample_email = "Please update me on the project status."

    # Patch the Ollama query function to avoid real API calls during test
    def fake_query_ollama(prompt):
        return "This is a test draft reply."

    # Replace the real function with fake one
    import backend.draft_generator as dg
    monkeypatch.setattr(dg, "query_ollama", fake_query_ollama)

    reply = generate_draft_reply(sample_email)
    assert isinstance(reply, str)
    assert "test draft reply" in reply.lower()
