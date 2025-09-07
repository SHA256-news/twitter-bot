import os
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

def main():
    headlines = get_latest_headlines()
    for headline in headlines:
        try:
            api.update_status(status=headline)
            print(f"Tweeted: {headline}")
        except Exception as e:
            print(f"Error tweeting: {e}")

if __name__ == "__main__":
    main()
