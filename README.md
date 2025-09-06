# twitter-bot
# SHA256 News Twitter Bot

This bot monitors RSS feeds for SHA256 Bitcoin mining news and tweets the latest headlines to Twitter.

## Features

- Fetches SHA256 Bitcoin mining news from RSS feeds
- Tweets headlines to a configured Twitter account
- Securely loads Twitter API credentials from a `.env` file (not included in repo)

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
   cd YOUR-REPO
   ```

2. **Create your `.env` file with Twitter API keys**  
   (See `.env.example` for format.)

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the bot:**
   ```sh
   python twitter_sha256_news_bot.py
   ```

## Deployment

You can deploy this bot using platforms like Render, Railway, or Fly.io (see deployment instructions in this repo).

## Security

- Secrets (API keys) are stored in `.env`, which is ignored by git via `.gitignore`.
- Never commit your `.env` with real secrets.

## License

MIT
