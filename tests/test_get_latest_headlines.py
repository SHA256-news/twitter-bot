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


def test_get_latest_headlines(monkeypatch):
    bot = import_bot(monkeypatch)

    class DummyRegistry:
        pass

    class DummyQuery:
        def __init__(self, keywords=None):
            self.keywords = keywords

        def execQuery(self, er):
            return [
                {"title": "Title 1", "url": "http://example.com/1"},
                {"title": "Title 2", "url": "http://example.com/2"},
                {"title": None, "url": "http://example.com/3"},
            ]

    class DummyItems:
        @staticmethod
        def AND(items):
            return items

    monkeypatch.setenv("NEWS_API_KEY", "key")
    monkeypatch.setenv("NEWS_QUERY", "python,ai")
    monkeypatch.setattr(bot, "EventRegistry", lambda apiKey=None: DummyRegistry())
    monkeypatch.setattr(bot, "QueryArticlesIter", DummyQuery)
    monkeypatch.setattr(bot, "QueryItems", DummyItems)

    headlines = bot.get_latest_headlines()
    assert headlines == [
        ("Title 1", "http://example.com/1"),
        ("Title 2", "http://example.com/2"),
    ]
