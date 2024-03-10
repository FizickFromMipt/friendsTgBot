import os
from collections import defaultdict

from googleapiclient.discovery import build
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, ParseMode, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, CallbackQueryHandler

# Оставляю пустым для гитхаба , ибо репозиторий публичный (при локальном запуске буду подставлять ручками сам)
TELEGRAM_BOT_TOKEN = ''
YOUTUBE_API_KEY = ''
YOUTUBE_CHANNEL_ID = 'efremovyobovsem'
YOUTUBE_CHANNEL_NAME = 'Ефремовы обо всём'
CHAT_ID = '-'

arr = [YOUTUBE_CHANNEL_NAME]
bot = Bot(token=TELEGRAM_BOT_TOKEN)
# Словарь для отслеживания количества сообщений каждого пользователя
user_message_count = defaultdict(int)

################### _КНОПКИ И КОМАНДЫ_ ##########################################

# Функция для создания основного меню
def get_main_menu():
    buttons = [
        [KeyboardButton("Старт")],
        [KeyboardButton("Информация о группе")],
        [KeyboardButton("Тест")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


#  функция для обработки команды /start
def start(update, context):
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Привет, {user.first_name}! персональный бот медиа-активности учатников данного чата.",
                             reply_markup=get_main_menu())


#  функция для обработки команды /start
def stats(update, context):
    chat_id = CHAT_ID
    stats_message = "Статистика сообщений:\n"

    for user_id, message_count in user_message_count.items():
        user = context.bot.get_chat_member(chat_id, user_id).user
        stats_message += f"{user.first_name} {user.last_name} ({user.username}): {message_count} сообщений\n"

    context.bot.send_message(chat_id=chat_id, text=stats_message)

# Информация про данный чат
def info(update, context):
    ##Подготовка инфы про чат
    chat_id = update.effective_chat.id
    members_count = context.bot.get_chat_member_count(chat_id) - 1

    text = ("<u>Информацию о данной группе</u>\n" +
                "\nКоличество учатников: " + (str)(members_count) +
                "\nАктивные подписки на каналы: " + (str)(arr))

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML)

# Функция для обработки нажатия на кнопку
def button_callback(update, context):
    query = update.callback_query
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы нажали на кнопку {query.data}")


# Ваша функция для обработки команды /chat_id
def chat_id(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=f"Идентификатор этого чата: {chat_id}")

def check_youtube(update, context):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    response = youtube.activities().list(
        part='snippet',
        channelId='efremovyobovsem',
    ).execute()

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=f"Ответ при запросе к ютубу: {response}")

#################################################################################



def check_youtube_activity(context: CallbackContext):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    response = youtube.activities().list(part='snippet', channelId=YOUTUBE_CHANNEL_ID).execute()

    context.bot.send_message(chat_id=context.job.context['chat_id'], text='Новая активность на YouTube!')

def handle_messages(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_message_count[user_id] += 1
    # Обработка всех входящих сообщений, кроме команд
    check_youtube_activity(context)

def main():
    updater = Updater(bot=bot)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("id", chat_id))
    dp.add_handler(CommandHandler("check", check_youtube))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))
    # dp.add_handler(CallbackQueryHandler(button_callback))
    # Запуск задачи по расписанию ( каждые 30 минут)
    updater.job_queue.run_repeating(check_youtube_activity, interval=15, context={'chat_id': CHAT_ID})

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()