Telegram News Bot

This is a Telegram bot that allows users to browse and select news articles using the [NewsAPI](https://newsapi.org). The bot provides an intuitive user experience by utilizing `InlineKeyboardButton` for easier navigation. All user data is stored in a database.

Features
- Fetches and displays news articles from [NewsAPI](https://newsapi.org)
- Users can navigate and select articles using inline buttons
- Stores user data in a PostgreSQL database

Technologies Used
- `python-telegram-bot` for Telegram bot functionality
- `asyncpg` for asynchronous PostgreSQL database interactions
- `requests` for fetching news from the API

Installation
1. Clone the repository:
   ```
   git clone [https://github.com/yourusername/telegram-news-bot.git https://github.com/Evgen-dev1989/telegram_bot.git](https://github.com/Evgen-dev1989/telegram_bot.git)
   cd telegram-news-bot
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up a PostgreSQL database and update your database credentials in the bot's configuration.
4. Obtain an API key from [NewsAPI](https://newsapi.org) and configure it in the bot.
5. Run the bot:
   ```
   python main.py
   ```
Usage
- Start the bot by sending `/start`.
- Choose a news category or search for specific topics.
- Use inline buttons to navigate between articles.

License
This project is licensed under the MIT License.

