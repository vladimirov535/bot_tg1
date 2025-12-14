import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# ================= НАСТРОЙКИ =================

VIDEO_FILE_ID = "BAACAgIAAxkBAAMTaT8DMTErXAugYxUU7GmGll78FTQAAimVAALjvPlJTIVl0usumb82BA"

URL_0 = "https://www.youtube.com/watch?v=QQ4N1oYfqH0"
URL_15 = "https://t.me/taobaobel11"
URL_24H = "https://taobaobel.by/taobao"
URL_50H = "https://t.me/taobaobel11"

BTN_0 = "Смотреть видео 🎥"
BTN_15 = "Написать менеджеру ✍️"
BTN_24H = "Смотреть программу 📘"
BTN_50H = "Написать менеджеру 💬"

TEXT_0 = (
    "Если вы рассматриваете <b>продажи на маркетплейсах</b> или хотите открыть "
    "<b>интернет-магазин</b> 🛒\n\n"
    "и думаете о поставках из Китая, но вас останавливают документы, таможня и "
    "«белый» ввоз — это видео для вас ✅\n\n"
    "📌 какие документы нужны\n"
    "💰 с какими суммами реально можно стартовать\n"
    "🧾 почему белый импорт сейчас — не страшно, а логично\n\n"
    "После просмотра вы поймёте, как заказывать из Китая с документами "
    "<b>партии от $300</b> 🚀"
)

TEXT_15 = (
    "Если вы посмотрели видео и подумали:\n\n"
    "«Как собрать всё в систему и не ошибиться?» 🤔\n\n"
    "Для этого нужен чёткий алгоритм.\n"
    "Я собрал его в обучении: шаги, документы и контакты 🧾📦\n\n"
    "Напишите менеджеру слово <b>«КИТАЙ»</b> 👇"
)

TEXT_24H = (
    "Напишу честно.\n\n"
    "<b>Белый импорт — это не сложно и не дорого</b> ❌\n"
    "Это про понимание процесса и цифр 📊\n\n"
    "Ниже — программа обучения, где я собрал всё, что использую на практике 👇"
)

TEXT_50H = (
    "Как зарабатывать <b>$850 в месяц</b>? 💵\n\n"
    "Работая байером и беря оптовые заказы 📦\n\n"
    "После обучения многие так и делают:\n"
    "— разбираются в белых поставках\n"
    "— берут заказы от $300\n"
    "— получают процент с каждой сделки 🤝\n\n"
    "<b>Напишите менеджеру «КИТАЙ»</b> и получите стоимость обучения 👇"
)

# ================= ВСПОМОГАТЕЛЬНЫЕ =================

def make_kb(text: str, url: str):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)]])

def job_name(chat_id: int, suffix: str):
    return f"{chat_id}:{suffix}"

# ================= ШАГИ =================

async def send_step_0(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_video(chat_id=chat_id, video=VIDEO_FILE_ID)
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_0,
        reply_markup=make_kb(BTN_0, URL_0),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

async def step_15(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_15,
        reply_markup=make_kb(BTN_15, URL_15),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

async def step_24h(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_24H,
        reply_markup=make_kb(BTN_24H, URL_24H),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

async def step_50h(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_50H,
        reply_markup=make_kb(BTN_50H, URL_50H),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await send_step_0(chat_id, context)

    jq = context.application.job_queue

    jq.run_once(step_15, when=15, name=job_name(chat_id, "15m"), data={"chat_id": chat_id})
    jq.run_once(step_24h, when=24 * 60 * 60, name=job_name(chat_id, "24h"), data={"chat_id": chat_id})
    jq.run_once(step_50h, when=50 * 60 * 60, name=job_name(chat_id, "50h"), data={"chat_id": chat_id})

    logging.info(f"Jobs scheduled for chat_id={chat_id}")

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
