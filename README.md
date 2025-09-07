# twitter-bot
# SHA256 News Twitter Bot

This bot uses NewsAPI's Python SDK to search for SHA256 Bitcoin mining news and tweets the latest headlines to Twitter.

## Features

- Fetches SHA256 Bitcoin mining news via NewsAPI queries
- Tweets headlines to a configured Twitter account
- Securely loads Twitter and NewsAPI credentials from a `.env` file (not included in repo)

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
   cd YOUR-REPO
   ```

2. **Create your `.env` file with Twitter API keys and NewsAPI settings**
   Copy `.env.example` and fill in:
   - `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`
   - `NEWS_API_KEY`: your NewsAPI key
   - `NEWS_QUERY`: search keywords for articles (e.g., `"SHA256 Bitcoin mining"`)

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the bot:**
   ```sh
   python twitter_sha256_news_bot.py
   ```

## NewsAPI usage example

```python
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
articles = newsapi.get_everything(q=os.getenv("NEWS_QUERY"))
```

## Deployment

You can deploy this bot using platforms like Render, Railway, or Fly.io (see deployment instructions in this repo).

## Security

- Secrets (API keys) are stored in `.env`, which is ignored by git via `.gitignore`.
- Never commit your `.env` with real secrets.

## License

MIT
