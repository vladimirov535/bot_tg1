import os
import logging
from datetime import datetime, timedelta, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Railway/Prod: твой публичный URL приложения (БЕЗ слэша в конце)
# Пример: https://bot-tg1-production.up.railway.app
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "").rstrip("/")
PORT = int(os.getenv("PORT", "8080"))

# =========================
# НАСТРОЙКИ КОНТЕНТА
# =========================

VIDEO_FILE_ID = "BAACAgIAAxkBAAMTaT8DMTErXAugYxUU7GmGll78FTQAAimVAALjvPlJTIVl0usumb82BA"
VIDEO_URL = ""  # если вдруг хочешь url mp4

INST_URL = "https://instagram.com/taobao_bel"  # <-- сюда свою инсту

URL_0 = "https://www.youtube.com/watch?v=QQ4N1oYfqH0"
URL_15 = "https://t.me/taobaobel11"
URL_24H = "https://taobaobel.by/taobao"
URL_50H = "https://t.me/taobaobel11"

BTN_0 = "Смотреть урок ✅"
BTN_15 = "Написать менеджеру 💬"
BTN_24H = "Смотреть программу 📚"
BTN_50H = "Написать менеджеру 💬"

TEXT_0 = """Если вы рассматриваете <b>продажи на маркетплейсах</b> или хотите открыть <b>свой интернет-магазин</b> и думаете о поставках из Китая, но вас останавливают документы, таможня и «белый» ввоз — это видео для вас. ✅

В нём я показываю, как на самом деле выстраиваются официальные поставки в Беларусь:

📌 — какие документы нужны  
💰 — с какими суммами реально можно стартовать  
🧾 — почему белый импорт сейчас — не страшно, а логично  

Посмотрите внимательно: после нашего обучения вы сможете заказывать из Китая с документами <b>партии от $300</b>."""

TEXT_15 = """Если вы уже посмотрели видео, скорее всего появилась мысль:

«Выглядит понятно, но как всё это собрать в одну систему и не ошибиться?»

Именно здесь большинство и застревает — не потому что сложно, а потому что нет чёткого алгоритма: что делать, в каком порядке и на что закладывать деньги.

✅ На обучении я собрал это в пошаговую структуру:  
— примеры всех документов  
— нужные контакты  
— базы поставщиков  

Напишите менеджеру слово <b>КИТАЙ</b> — и вам пришлют тарифы 👇"""

TEXT_24H = """Напишу честно.

<b>Белый импорт — это не про «сложно и дорого»</b>.  
Это про понимание процесса, цифр и рисков.

Если вы планируете привозить и продавать товары из Китая — <b>разобраться один раз намного выгоднее</b>, чем постоянно действовать наугад.

Ниже — программа обучения, где я собрал всё, что сам использую на практике 👇"""

TEXT_50H = """Как зарабатывать <b>$850 в месяц</b>?

Можно начать работать байером и брать оптовые заказы. Некоторые ребята после обучения делают именно так:

📦 Разбираетесь с белыми поставками  
🤝 Берёте оптовые (или небольшие от $300) заказы  
💵 Получаете свой % от сделки  

Как подработка — <b>$850 в месяц вполне реально</b>.  
Ваши знания точно будут стоить денег.

<b>Напишите слово КИТАЙ</b> менеджеру — и получите стоимость обучения 👇"""

# =========================
# КНОПКИ
# =========================

def kb_one(text: str, url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)]])

def kb_two_rows(main_text: str, main_url: str) -> InlineKeyboardMarkup:
    # 1-я строка: основная кнопка
    # 2-я строка: Instagram
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(main_text, url=main_url)],
        [InlineKeyboardButton("Перейти в Instagram 📸", url=INST_URL)],
    ])

def job_name(chat_id: int, suffix: str) -> str:
    return f"{chat_id}:{suffix}"

def remove_existing_jobs(app: Application, chat_id: int):
    for suffix in ("15m", "24h", "50h"):
        name = job_name(chat_id, suffix)
        for job in app.job_queue.get_jobs_by_name(name):
            job.schedule_removal()

# =========================
# ОТПРАВКИ ШАГОВ
# =========================

async def send_step_0(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    # Видео
    if VIDEO_FILE_ID:
        await context.bot.send_video(chat_id=chat_id, video=VIDEO_FILE_ID)
    elif VIDEO_URL:
        await context.bot.send_video(chat_id=chat_id, video=VIDEO_URL)
    else:
        await context.bot.send_message(chat_id=chat_id, text="(Видео пока не настроено)")

    # Текст + кнопки (2 строки: основная + Instagram)
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_0,
        reply_markup=kb_two_rows(BTN_0, URL_0),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

async def step_15_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_15,
        reply_markup=kb_two_rows(BTN_15, URL_15),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

async def step_24h_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_24H,
        reply_markup=kb_two_rows(BTN_24H, URL_24H),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

async def step_50h_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_50H,
        reply_markup=kb_two_rows(BTN_50H, URL_50H),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

# =========================
# /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # 1) Сразу отправка
    await send_step_0(chat_id, context)

    # 2) Если /start нажали повторно — убираем старые таймеры
    remove_existing_jobs(context.application, chat_id)

    # 3) Планируем отложенные сообщения
    context.job_queue.run_once(
        step_15_job,
        when=15 * 60,
        name=job_name(chat_id, "15m"),
        data={"chat_id": chat_id},
    )
    context.job_queue.run_once(
        step_24h_job,
        when=24 * 60 * 60,
        name=job_name(chat_id, "24h"),
        data={"chat_id": chat_id},
    )
    context.job_queue.run_once(
        step_50h_job,
        when=50 * 60 * 60,
        name=job_name(chat_id, "50h"),
        data={"chat_id": chat_id},
    )

# =========================
# file_id видео (если нужно)
# =========================

async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(f"VIDEO_FILE_ID:\n{file_id}")
    else:
        await update.message.reply_text("Пришлите видеофайл (не ссылку), чтобы я дал file_id.")

# =========================
# ERROR HANDLER (чтобы видеть ошибки)
# =========================

async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception("Unhandled error: %s", context.error)

def build_app() -> Application:
    if not TOKEN:
        raise ValueError("No TELEGRAM_TOKEN in environment variables")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_video_id", get_video_id))
    app.add_handler(MessageHandler(filters.VIDEO, get_video_id))

    app.add_error_handler(on_error)
    return app

def main():
    app = build_app()

    # ===== PROD (WEBHOOK) =====
    if WEBHOOK_BASE_URL:
        # Будет URL вида: https://domain/<TOKEN>
        webhook_path = f"/{TOKEN}"
        webhook_url = f"{WEBHOOK_BASE_URL}{webhook_path}"

        logger.info("Starting webhook on port %s, webhook_url=%s", PORT, webhook_url)

        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,           # важно: без слэша
            webhook_url=webhook_url,  # публичный URL
            drop_pending_updates=True,
        )
        return

    # ===== DEV (POLLING) =====
    logger.info("Starting polling (DEV mode). Set WEBHOOK_BASE_URL for production.")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
