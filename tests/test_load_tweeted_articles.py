import importlib
import sys
from pathlib import Path


def test_load_tweeted_articles_handles_invalid_json(monkeypatch, tmp_path):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    bot = importlib.import_module("twitter_sha256_news_bot")

    # Ensure no real API is created during tests
    monkeypatch.setattr(bot, "create_api", lambda: None)

    store = tmp_path / "tweeted_articles.json"
    store.write_text("{invalid")
    monkeypatch.setattr(bot, "STORE_FILE", str(store))

    assert bot.load_tweeted_articles() == {}


def test_load_tweeted_articles_handles_oserror(monkeypatch, tmp_path):
    monkeypatch.setenv("TWITTER_API_KEY", "x")
    monkeypatch.setenv("TWITTER_API_SECRET", "x")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN", "x")
    monkeypatch.setenv("TWITTER_ACCESS_TOKEN_SECRET", "x")

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    bot = importlib.import_module("twitter_sha256_news_bot")

    store = tmp_path / "tweeted_articles.json"
    store.write_text("{}")
    monkeypatch.setattr(bot, "STORE_FILE", str(store))

    def raise_oserror(*args, **kwargs):
        raise OSError("boom")

    monkeypatch.setattr("builtins.open", raise_oserror)

    assert bot.load_tweeted_articles() == {}
