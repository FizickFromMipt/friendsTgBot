import os
from googleapiclient.discovery import build
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

# Оставляю пустым для гитхаба , ибо репозиторий публичный (при локальном запуске буду подставлять ручками сам)
TELEGRAM_BOT_TOKEN = ''
YOUTUBE_API_KEY = ''
YOUTUBE_CHANNEL_ID = '@efremovyobovsem'

def start(update, context):
    update.message.reply_text('Привет! Я бот для отслеживания активности на YouTube канале.')

def check_youtube_activity(context: CallbackContext):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    response = youtube.activities().list(part='snippet', channelId=YOUTUBE_CHANNEL_ID).execute()

    # Обработка данных активности на канале (можно настроить для разных типов событий)

    # Пример: отправка уведомления в Telegram
    context.bot.send_message(chat_id=context.job.context['chat_id'], text='Новая активность на YouTube!')

def handle_messages(update, context):
    # Обработка всех входящих сообщений, кроме команд
    check_youtube_activity(context)

def main():
    updater = Updater(bot=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(~CommandHandler & ~CallbackContext, handle_messages))

    # Запуск задачи по расписанию (например, каждые 30 минут)
    updater.job_queue.run_repeating(check_youtube_activity, interval=1800, context={'chat_id': '-1002108450567'})

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()