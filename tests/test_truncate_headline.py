import importlib
import re
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


def test_truncate_headline_accounts_for_url_length(monkeypatch):
    bot = import_bot(monkeypatch)
    long_text = "A" * 270
    url = (
        "https://example.com/this-is-a-very-long-url-that-exceeds-twitter-shortened-length"
    )
    headline = f"{long_text} {url}"
    truncated = bot.truncate_headline(headline)
    assert truncated == f"{'A' * 256} {url}"
    urls = re.findall(r"https?://\S+", truncated)
    effective_length = len(truncated) + sum(23 - len(u) for u in urls)
    assert effective_length <= 280


def test_truncate_headline_keeps_only_last_url(monkeypatch):
    bot = import_bot(monkeypatch)
    headline = "start http://one.com middle http://two.com"
    result = bot.truncate_headline(headline, max_length=30)
    assert "http://one.com" not in result
    assert result.strip().endswith("http://two.com")
    urls = re.findall(r"https?://\S+", result)
    effective_length = len(result) + sum(23 - len(u) for u in urls)
    assert effective_length <= 30
