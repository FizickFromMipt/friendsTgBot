import asyncio
from telegram import Bot

async def get_chat_info():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    bot = Bot(token='6382716824:AAH-jD8qDPWWxAiWH2YHpJn4JvMF8UxW9K8')

    # Замените @your_channel_username на юзернейм вашего канала или группы
    chat_id = '@your_channel_username'

    # Получите информацию о чате
    chat_info = await bot.get_chat(chat_id)

    # Выведите Chat ID
    print(f"Chat Title: {chat_info.title}, Chat ID: {chat_info.id}")

# Запустите асинхронный код
asyncio.run(get_chat_info())

