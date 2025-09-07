import os
import re
import json
import time
import logging

from eventregistry import EventRegistry, QueryArticlesIter, QueryItems
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials from .env
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Validate credentials before authenticating
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise RuntimeError(
        "Missing Twitter API credentials. Ensure TWITTER_API_KEY, "
        "TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN and "
        "TWITTER_ACCESS_TOKEN_SECRET are set."
    )

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

# Persistent store for tweeted article URLs
STORE_FILE = "tweeted_articles.json"
RETENTION_DAYS = 7

logger = logging.getLogger(__name__)


def load_tweeted_articles():
    if os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_tweeted_articles(data):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def cleanup_old_entries(data):
    threshold = time.time() - RETENTION_DAYS * 24 * 60 * 60
    removed = [url for url, ts in data.items() if ts < threshold]
    for url in removed:
        del data[url]
    return removed

def get_latest_headlines():
    """Fetch recent article titles and URLs from EventRegistry."""
    api_key = os.getenv("NEWS_API_KEY")
    query_terms = os.getenv("NEWS_QUERY")
    if not api_key:
        raise RuntimeError("NEWS_API_KEY environment variable is not set.")
    if not query_terms:
        raise RuntimeError("NEWS_QUERY environment variable is not set.")

    headlines = []
    try:
        er = EventRegistry(apiKey=api_key)
        keywords = QueryItems.AND(query_terms.split(","))
        query = QueryArticlesIter(keywords=keywords)
        for article in query.execQuery(er):
            title = article.get("title")
            url = article.get("url")
            if title and url:
                headlines.append((title, url))
            if len(headlines) >= 5:
                break
    except Exception as e:
        logger.error("Error fetching headlines: %s", e)
        return []
    return headlines


def truncate_headline(headline: str, max_length: int = 280) -> str:
    """Truncate headline to fit within Twitter's character limit.

    Twitter wraps URLs with t.co, reducing each URL to 23 characters
    regardless of its original length. This function accounts for that
    shortening when calculating the effective length of a tweet.

    Parameters
    ----------
    headline: str
        The headline text, typically including a URL.
    max_length: int
        Maximum allowed length for the tweet. Default is 280 characters.

    Returns
    -------
    str
        The headline truncated to fit within the length constraint.
    """

    urls = re.findall(r"https?://\S+", headline)
    effective_length = len(headline) + sum(23 - len(url) for url in urls)
    if effective_length <= max_length:
        return headline

    if urls:
        # Keep only the last URL (assumed to be at the end of the headline)
        last_url = urls[-1]
        prefix = headline[: headline.rfind(last_url)].rstrip()
        allowed = max_length - 23 - (1 if prefix else 0)
        return f"{prefix[:allowed]}{' ' if prefix else ''}{last_url}"

    return headline[:max_length]

def main():
    tweeted = load_tweeted_articles()
    cleanup_old_entries(tweeted)
    save_tweeted_articles(tweeted)

    headlines = get_latest_headlines()
    for title, url in headlines:
        if url in tweeted:
            print(f"Skipping already tweeted article: {url}")
            continue
        try:
            tweet = truncate_headline(f"{title} {url}")
            api.update_status(status=tweet)
            tweeted[url] = time.time()
            save_tweeted_articles(tweeted)
            print(f"Tweeted: {title} {url}")
        except Exception as e:
            print(f"Error tweeting: {e}")

if __name__ == "__main__":
    main()
