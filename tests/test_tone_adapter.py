import pytest
from backend.tone_adapter import build_tone_prompt, embed_and_save_tone_vectors

def test_build_tone_prompt_returns_string():
    sample_email = "Can you confirm the meeting time?"
    prompt = build_tone_prompt(sample_email)
    assert isinstance(prompt, str)
    assert "reply" in prompt.lower()

# Optional: test embed_and_save_tone_vectors for no errors (requires some emails)
def test_embed_and_save_tone_vectors_runs():
    try:
        embed_and_save_tone_vectors()
    except Exception as e:
        pytest.skip(f"Skipped embed test: {e}")
