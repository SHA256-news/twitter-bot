import os
import feedparser
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

# RSS feeds from .env (comma-separated)
RSS_FEEDS = [url.strip() for url in os.getenv("RSS_FEEDS", "").split(",") if url.strip()]

def get_latest_headlines(feed_url):
    headlines = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:5]:  # Get top 5 headlines
        headlines.append(f"{entry.title} {entry.link}")
    return headlines

def main():
    if not RSS_FEEDS:
        print("No RSS feeds configured. Set RSS_FEEDS in environment.")
        return

    for feed_url in RSS_FEEDS:
        headlines = get_latest_headlines(feed_url)
        for headline in headlines:
            try:
                api.update_status(status=headline)
                print(f"Tweeted: {headline}")
            except Exception as e:
                print(f"Error tweeting: {e}")

if __name__ == "__main__":
    main()
