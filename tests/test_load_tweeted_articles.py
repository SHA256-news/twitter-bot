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
