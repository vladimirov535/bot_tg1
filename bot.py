import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# === НАСТРОЙКИ (замени под себя) ===
# ================= НАСТРОЙКИ =================

# ВИДЕО:
# 1) Лучше всего вставить file_id (после того как получим его)
VIDEO_FILE_ID = "BAACAgIAAxkBAAMTaT8DMTErXAugYxUU7GmGll78FTQAAimVAALjvPlJTIVl0usumb82BA"

# Если file_id нет, можно вставить URL на видео (но не всегда стабильно)
VIDEO_URL = ""  # пример: "https://....mp4"

# Ссылки для кнопок
URL_0 = "https://www.youtube.com/watch?v=QQ4N1oYfqH0"
URL_15 = "https://t.me/taobaobel11"
URL_24H = "https://taobaobel.by/taobao"
URL_50H = "https://t.me/taobaobel11"

# Тексты сообщений
BTN_0 = "Смотреть видео 🎥"
BTN_15 = "Написать менеджеру ✍️"
BTN_24H = "Смотреть программу 📘"
BTN_50H = "Написать менеджеру 💬"

TEXT_0 = (
    "Если вы рассматриваете <b>продажи на маркетплейсах</b> или хотите открыть свой <b>интернет-магазин</b> 🛒\n"
    "и думаете о поставках из Китая, но вас останавливают документы, таможня и «белый» ввоз — это видео для вас ✅\n\n"
    "В нём я показываю, как на самом деле выстраиваются официальные поставки в Беларусь 🇧🇾:\n\n"
    "📌 что за документы нужны\n"
    "Если вы рассматриваете <b>продажи на маркетплейсах</b> или хотите открыть "
    "<b>интернет-магазин</b> 🛒\n\n"
    "и думаете о поставках из Китая, но вас останавливают документы, таможня и "
    "«белый» ввоз — это видео для вас ✅\n\n"
    "📌 какие документы нужны\n"
    "💰 с какими суммами реально можно стартовать\n"
    "🧾 почему белый импорт сейчас — не страшно, а логично\n\n"
    "Посмотрите внимательно — рассказываю, как после нашего обучения вы сможете заказывать из Китая с документами <b>партии от $300</b> 🚀"
    "После просмотра вы поймёте, как заказывать из Китая с документами "
    "<b>партии от $300</b> 🚀"
)


TEXT_15 = (
    "Если вы уже посмотрели видео, скорее всего появилась мысль:\n\n"
    "«Выглядит понятно, но как всё это собрать в одну систему и не ошибиться?» 🤔\n\n"
    "Именно здесь многие и застревают — не потому что сложно, а потому что нет чёткого алгоритма:\n"
    "что делать, в каком порядке и на что закладывать деньги 💰\n\n"
    "В обучении я собрал это в пошаговую структуру ✅\n"
    "С примерами документов 🧾, контактами и базами поставщиков 📦\n\n"
    "Напишите менеджеру слово <b>«КИТАЙ»</b> — и вам пришлют тарифы обучения 👇"
    "Если вы посмотрели видео и подумали:\n\n"
    "«Как собрать всё в систему и не ошибиться?» 🤔\n\n"
    "Для этого нужен чёткий алгоритм.\n"
    "Я собрал его в обучении: шаги, документы и контакты 🧾📦\n\n"
    "Напишите менеджеру слово <b>«КИТАЙ»</b> 👇"
)



TEXT_24H = (
    "Напишу честно.\n\n"
    "<b>Белый импорт — это не про «сложно и дорого»</b> ❌\n"
    "Это про понимание процесса, цифр и рисков 📊\n\n"
    "Если вы планируете привозить и продавать товары из Китая, то "
    "<b>разобраться в этом один раз — намного выгоднее</b>, "
    "чем постоянно действовать наугад и терять деньги 💸\n\n"
    "Ниже — программа обучения, где я собрал всё, что сам использую на практике 👇"
    "<b>Белый импорт — это не сложно и не дорого</b> ❌\n"
    "Это про понимание процесса и цифр 📊\n\n"
    "Ниже — программа обучения, где я собрал всё, что использую на практике 👇"
)



TEXT_50H = (
    "Как зарабатывать <b>$850 в месяц?</b> 💵\n\n"
    "Начать работать байером и брать оптовые заказы 📦\n\n"
    "Некоторые участники после нашего обучения выбирают именно этот путь:\n\n"
    "— разбираются с белыми поставками 🧾\n"
    "— берут оптовые (или небольшие от $300) заказы\n"
    "— получают свой процент с каждой сделки 🤝\n\n"
    "<b>Как подработка $850 в месяц — это реально.</b>\n"
    "Ваши знания и навыки начинают приносить деньги 💰\n\n"
    "Присоединяйтесь к обучению и получите понятный и рабочий способ\n"
    "зарабатывать дополнительные $ к основной работе 🚀\n\n"
    "<b>Напишите менеджеру слово «КИТАЙ» и получите стоимость обучения 👇</b>"
    "Как зарабатывать <b>$850 в месяц</b>? 💵\n\n"
    "Работая байером и беря оптовые заказы 📦\n\n"
    "После обучения многие так и делают:\n"
    "— разбираются в белых поставках\n"
    "— берут заказы от $300\n"
    "— получают процент с каждой сделки 🤝\n\n"
    "<b>Напишите менеджеру «КИТАЙ»</b> и получите стоимость обучения 👇"
)

BTN_0 = "Смотреть видео✅"
BTN_15 = "Написать"
BTN_24H = "Смотреть программу"
BTN_50H = "Написать менеджеру"
# ================= ВСПОМОГАТЕЛЬНЫЕ =================

# Имена job'ов, чтобы можно было отменять старые
def job_name(chat_id: int, suffix: str) -> str:
    return f"{chat_id}:{suffix}"
def make_kb(text: str, url: str):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)]])

def job_name(chat_id: int, suffix: str):
    return f"{chat_id}:{suffix}"

def make_kb(button_text: str, url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=url)]])

# ================= ШАГИ =================

async def send_step_0(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    # Видео
    if VIDEO_FILE_ID:
        await context.bot.send_video(
            chat_id=chat_id,
            video=VIDEO_FILE_ID
        )
    elif VIDEO_URL:
        await context.bot.send_video(
            chat_id=chat_id,
            video=VIDEO_URL
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="(Видео пока не настроено)"
        )

    # Сообщение + кнопка
    await context.bot.send_video(chat_id=chat_id, video=VIDEO_FILE_ID)
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_0,
        parse_mode="HTML",
        reply_markup=make_kb(BTN_0, URL_0),
        disable_web_page_preview=True,
        parse_mode="HTML",
        disable_web_page_preview=True
    )




async def step_15_job(context: ContextTypes.DEFAULT_TYPE):
async def step_15(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_15,
        parse_mode="HTML",
        reply_markup=make_kb(BTN_15, URL_15),
        disable_web_page_preview=True,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


async def step_24h_job(context: ContextTypes.DEFAULT_TYPE):
async def step_24h(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_24H,
        parse_mode="HTML",
        reply_markup=make_kb(BTN_24H, URL_24H),
        disable_web_page_preview=True,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


async def step_50h_job(context: ContextTypes.DEFAULT_TYPE):
async def step_50h(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(
        chat_id=chat_id,
        text=TEXT_50H,
        parse_mode="HTML",
        reply_markup=make_kb(BTN_50H, URL_50H),
        disable_web_page_preview=True,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


def remove_existing_jobs(app, chat_id: int):
    # на случай, если человек нажимает /start несколько раз — отменяем старые таймеры
    for suffix in ("15m", "24h", "50h"):
        name = job_name(chat_id, suffix)
        for job in app.job_queue.get_jobs_by_name(name):
            job.schedule_removal()

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # 1) Сразу отправляем видео + сообщение + кнопка
    await send_step_0(chat_id, context)

    # 2) Убираем старые jobs (если /start нажали повторно)
    remove_existing_jobs(context.application, chat_id)

    # 3) Планируем отложенные сообщения
    # через 15 минут = 15 * 60
    context.job_queue.run_once(
        step_15_job,
        when=20,
        name=job_name(chat_id, "15m"),
        data={"chat_id": chat_id},
    )

    # через сутки = 24 * 60 * 60
    context.job_queue.run_once(
        step_24h_job,
        when=24 * 60 * 60,
        name=job_name(chat_id, "24h"),
        data={"chat_id": chat_id},
    )
    jq = context.application.job_queue

    # еще через 50 часов (я трактую как "через 50 часов от старта")
    # 50 * 60 * 60
    context.job_queue.run_once(
        step_50h_job,
        when=50 * 60 * 60,
        name=job_name(chat_id, "50h"),
        data={"chat_id": chat_id},
    )
    jq.run_once(step_15, when=15 * 60, name=job_name(chat_id, "15m"), data={"chat_id": chat_id})
    jq.run_once(step_24h, when=24 * 60 * 60, name=job_name(chat_id, "24h"), data={"chat_id": chat_id})
    jq.run_once(step_50h, when=50 * 60 * 60, name=job_name(chat_id, "50h"), data={"chat_id": chat_id})

    logging.info(f"Jobs scheduled for chat_id={chat_id}")

# (опционально) Команда для получения file_id видео:
# отправляешь видео боту -> он отвечает file_id
async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(f"VIDEO_FILE_ID:\n{file_id}")
    else:
        await update.message.reply_text("Пришли мне именно видеофайл (не ссылку), чтобы я дал file_id.")

# ================= MAIN =================

def main():
    if not TOKEN:
        raise ValueError("No TELEGRAM_TOKEN in environment variables")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # включи на время, чтобы получить file_id:
    app.add_handler(CommandHandler("get_video_id", get_video_id))
    app.add_handler(MessageHandler(filters.VIDEO, get_video_id))

    app.run_polling()
    app.run_polling(drop_pending_updates=True)
    app.run_polling(drop_pending_updates=True)

    # держим процесс живым
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()

