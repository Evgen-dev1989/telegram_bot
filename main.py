from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import asyncio
import asyncpg
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import nest_asyncio
#from db import user, password, database, host, port, token

nest_asyncio.apply()
token = "7790924699:AAGpKDdYpp9jjYgiJHqtkLINR9GVR9keq20"
host = 'localhost'
port = 5432 
database = 'telegram'
password = "1111"
user = 'postgres'


create_db = (
    """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL,
            time TIMESTAMP DEFAULT NOW(),
            user_id INTEGER PRIMARY KEY NOT NULL,
            user_name VARCHAR(250) NOT NULL,
            first_name VARCHAR(250),
            last_name VARCHAR(250)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS categories (
            user_id INTEGER,
            category VARCHAR(100),
            time TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (user_id )
            REFERENCES users (user_id )
            ON UPDATE CASCADE
            ON DELETE CASCADE
)
    """
)

async def connect_db():

    return await asyncpg.connect(user=user, password=password, database=database, host=host, port=port)


async def command_execute(command, arguments = None):

    conn = None
    try:
        conn = await connect_db()
        if arguments is not None:
            await conn.execute(command, *arguments)
        else :
            await conn.execute(command)

    except asyncpg.PostgresError as e:
        raise e
    
    finally:
        if conn is not None:  
            await conn.close()


def create_keyboard(buttons):

    keyboard = [[InlineKeyboardButton(text=button['text'], callback_data=button['callback_data'])] for button in buttons]
    return InlineKeyboardMarkup(keyboard)

  
buttons = [
    {'text': 'Health', 'callback_data': 'health'},
    {'text': 'Business', 'callback_data': 'business'},
    {'text': 'Entertainment', 'callback_data': 'entertainment'},
    {'text': 'General', 'callback_data': 'general'},
    {'text': 'Science', 'callback_data': 'science'},
    {'text': 'Sports', 'callback_data': 'sports'},
    {'text': 'Technology', 'callback_data': 'technology'}
    ]
reply_markup = create_keyboard(buttons)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    conn = None
    try:
        conn = await connect_db()
        user_id = update.effective_user.id
        user_name = update.effective_user.username
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
    
        record = await conn.fetchval('SELECT user_id FROM users WHERE user_id = $1', user_id)

        if record is None:  
            insert_query = """
            INSERT INTO users(time, user_id, user_name, first_name, last_name) 
            VALUES (NOW(), $1, $2, $3, $4);
            """
            await command_execute(insert_query, [user_id, user_name, first_name, last_name])
        await update.message.reply_text(f"Hello {first_name}. Do you want to read news?")
    except asyncpg.PostgresError as e:
        print(f"Database error: {str(e)}") 

    
    finally:
        if conn is not None:  
            await conn.close()


def get_news(category):

    params = {
        'sortBy': 'top',
        'language': 'en',
        'category': category,
        'country': 'us',
        'apiKey': '99a2323493084f53b211e6ed56a4921c',
    }

    url = 'https://newsapi.org/v2/top-headlines'
    try:
        response = requests.get(url, params=params)

        data = response.json()

        ready_news = []

        for article in data['articles']:
            news_item = {
                'title': article.get('title'),
                'url': article.get('url')
            }
            ready_news.append(news_item)

        return ready_news
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
    

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text('Choose your category:', reply_markup=reply_markup)


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    query = update.callback_query
    await query.answer() 
    category = query.data 
    await send_news(update, context, category)


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if context.args:
        category = " ".join(context.args)  
        await send_news(update, context, category)
    else:
        await update.message.reply_text(
            "Please choose one category using the buttons below.",
            reply_markup=reply_markup
        )


async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str) -> None:
 
    category_info = get_news(category)

    if update.message:
        message = update.message
    elif update.callback_query:
        message = update.callback_query.message
    else:
        return 

    if category_info:
        for article in category_info:
            await message.reply_text(f"{article['title']}\n{article['url']}")
    else:
        await message.reply_text(f"No news found for category: {category}")

async def main():

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("category", news))  
    application.add_handler(CallbackQueryHandler(handle_callback_query))  
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  

    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
