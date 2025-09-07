import importlib
import sys
from pathlib import Path


def import_bot(monkeypatch):
    monkeypatch.setenv("TWITTER_API_KEY", "x")
    monkeypatch.setenv("TWITTER_API_SECRET", "x")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN", "x")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN_SECRET", "x")
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    if "twitter_sha256_news_bot" in sys.modules:
        del sys.modules["twitter_sha256_news_bot"]
    return importlib.import_module("twitter_sha256_news_bot")


def test_cleanup_old_entries(monkeypatch):
    bot = import_bot(monkeypatch)
    now = 1_000_000
    monkeypatch.setattr(bot.time, "time", lambda: now)
    threshold = now - bot.RETENTION_DAYS * 24 * 60 * 60
    data = {
        "http://old.com": threshold - 1,
        "http://new.com": threshold + 1,
    }
    removed = bot.cleanup_old_entries(data)
    assert removed == ["http://old.com"]
    assert "http://old.com" not in data
    assert "http://new.com" in data
