import pytest
from main import resolve_theme, get_api_key

def test_resolve_theme_known():
    assert resolve_theme("fen") == "my4gypek52gile2"
    assert resolve_theme("onyx") == "onyx"

def test_resolve_theme_id_direct():
    assert resolve_theme("abc123def456") == "abc123def456"

def test_resolve_theme_partial():
    assert resolve_theme("anticip") == "e5ukwaw8omaqad3"

def test_get_api_key_missing(monkeypatch):
    monkeypatch.delenv("GAMMA_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        get_api_key()

def test_get_api_key_present(monkeypatch):
    monkeypatch.setenv("GAMMA_API_KEY", "test-key")
    assert get_api_key() == "test-key"
