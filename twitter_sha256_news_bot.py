import os
import re
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
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_latest_headlines():
    """Fetch recent article titles and URLs from EventRegistry."""
    er = EventRegistry(apiKey=os.getenv("NEWS_API_KEY"))
    keywords = QueryItems.AND(os.getenv("NEWS_QUERY", "").split(","))
    query = QueryArticlesIter(keywords=keywords)
    headlines = []
    for article in query.execQuery(er):
        title = article.get("title")
        url = article.get("url")
        if title and url:
            headlines.append(f"{title} {url}")
        if len(headlines) >= 5:
            break
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
    headlines = get_latest_headlines()
    for headline in headlines:
        try:
            tweet = truncate_headline(headline)
            api.update_status(status=tweet)
            print(f"Tweeted: {headline}")
        except Exception as e:
            print(f"Error tweeting: {e}")

if __name__ == "__main__":
    main()
