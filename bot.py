from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")  # токен берём из переменных окружения

# сюда вставь ссылку на свой лид-магнит (гугл-диск, лендинг, гидкурс и т.п.)
LEAD_MAGNET_URL = "https://example.com/lead-magnet"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Получить подарок 🎁"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    text = (
        "Привет! 👋\n\n"
        "Я бот, который выдаёт тебе подарок.\n"
        "Нажми кнопку ниже, чтобы получить лид-магнит 🎁"
    )
    await update.message.reply_text(text, reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # любое сообщение → выдаём подарок
    answer = (
        "Держи твой подарок 🎁\n\n"
        f"{LEAD_MAGNET_URL}\n\n"
        "Если ссылка не открылась — скопируй её и вставь в браузер."
    )
    await update.message.reply_text(answer)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен на сервере")
    app.run_polling()


if __name__ == "__main__":
    main()

