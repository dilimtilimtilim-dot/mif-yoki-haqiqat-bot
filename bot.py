import os
import logging
from html import escape

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes,
)

# Bot tokenni @BotFather orqali oling va BOT_TOKEN muhit o'zgaruvchisiga kiriting.
TOKEN = os.getenv("BOT_TOKEN", "").strip()
if not TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi. .env fayl yoki muhit o'zgaruvchisiga bot tokenini kiriting.")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

QUIZ = [
    {
        "q": "Gripp virusli infeksiya hisoblanadi.",
        "a": "HAQIQAT",
        "why": "Grippga influenza viruslari sabab bo'ladi.",
    },
    {
        "q": "Antibiotiklar gripp virusini bevosita yo'q qiladi.",
        "a": "MIF",
        "why": "Antibiotiklar bakteriyalarga qarshi ishlaydi, viruslarga emas.",
    },
    {
        "q": "Grippda isitma, bosh og'rig'i va mushak og'rig'i kuzatilishi mumkin.",
        "a": "HAQIQAT",
        "why": "Bular grippning keng tarqalgan belgilaridir.",
    },
    {
        "q": "Paragripp bolalarda soxta krup va huruvchi yo'talga sabab bo'lishi mumkin.",
        "a": "HAQIQAT",
        "why": "Paragripp hiqildoq va yuqori nafas yo'llarini zararlashi mumkin.",
    },
    {
        "q": "Adenovirus faqat nafas yo'llarini zararlaydi.",
        "a": "MIF",
        "why": "Adenovirus ko'z, ichak va boshqa a'zolarni ham zararlashi mumkin.",
    },
    {
        "q": "Qo'lni sovun bilan muntazam yuvish infeksiya tarqalishini kamaytiradi.",
        "a": "HAQIQAT",
        "why": "Qo'l gigiyenasi infeksiya profilaktikasining muhim qismidir.",
    },
    {
        "q": "Gripp bilan kasallangan har bir bolaga antibiotik berish shart.",
        "a": "MIF",
        "why": "Antibiotiklar faqat bakterial infeksiya bo'lsa yoki shifokor asos topsa qo'llanadi.",
    },
    {
        "q": "PCR yoki NAAT tekshiruvlari virusning genetik materialini aniqlashi mumkin.",
        "a": "HAQIQAT",
        "why": "PCR — NAAT usullaridan biri; bu testlar virus DNKsi yoki RNKsini aniqlashi mumkin.",
    },
    {
        "q": "Bola nafas olishda qiynalsa, uyda kuzatishning o'zi yetarli.",
        "a": "MIF",
        "why": "Nafas qisilishi shoshilinch tibbiy baholashni talab qiladi.",
    },
    {
        "q": "Grippga qarshi emlash kasallanish va og'ir asoratlar xavfini kamaytirishi mumkin.",
        "a": "HAQIQAT",
        "why": "Mavsumiy gripp vaksinasi kasallik va og'ir kechish xavfini kamaytirishga yordam beradi.",
    },
    {
        "q": "Antibiotiklarni shifokor tavsiyasisiz o'zboshimchalik bilan berish xavfsiz.",
        "a": "MIF",
        "why": "O'zboshimchalik bilan antibiotik berish nojo'ya ta'sirlar va antibiotiklarga chidamlilik xavfini oshiradi.",
    },
    {
        "q": "Xonani muntazam shamollatish va yo'tal odobiga rioya qilish infeksiya tarqalishini kamaytirishga yordam beradi.",
        "a": "HAQIQAT",
        "why": "Shamollatish, yo'talganda og'iz-burnini berkitish va qo'l gigiyenasi profilaktikaga yordam beradi.",
    },
    {
        "q": "Gripp va paragripp aynan bir virus sababli yuzaga keladi.",
        "a": "MIF",
        "why": "Ularni turli viruslar keltirib chiqaradi; belgilari ayrim jihatdan o'xshash bo'lishi mumkin.",
    },
    {
        "q": "Bolada lablar ko'karishi, hushyorlik pasayishi yoki nafas olish qiyinlashishi xavf belgilaridir.",
        "a": "HAQIQAT",
        "why": "Bunday belgilar paydo bo'lsa, zudlik bilan shoshilinch tibbiy yordamga murojaat qilish kerak.",
    },
    {
        "q": "Virusli respirator infeksiyada suyuqlik ichish va bolaning holatini kuzatish parvarishning muhim qismidir.",
        "a": "HAQIQAT",
        "why": "Yetarli suyuqlik va holatni kuzatish muhim; davolash bolaning yoshi, belgilari va shifokor tavsiyasiga mos bo'lishi kerak.",
    },
]

def quiz_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🟢 HAQIQAT", callback_data="answer:HAQIQAT"),
            InlineKeyboardButton("🔴 MIF", callback_data="answer:MIF"),
        ],
        [InlineKeyboardButton("⏹ O'yinni tugatish", callback_data="finish")],
    ])

def start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 O'yinni boshlash", callback_data="begin")],
        [InlineKeyboardButton("📤 Ulashish yo'riqnomasi", callback_data="share_help")],
    ])

def session(context):
    return context.user_data.get("quiz_session")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /start share payload bo'lsa ham o'yin taklifini ko'rsatamiz.
    name = update.effective_user.first_name if update.effective_user else "ishtirokchi"
    text = (
        f"Salom, {escape(name)}! 👋\n\n"
        "🧠 <b>“Mif yoki haqiqat?”</b>\n"
        "Bolalarda gripp, paragripp va adenovirus infeksiyalari bo'yicha 15 savolli viktorina.\n\n"
        "Har savolga javob berganingizdan keyin javobingiz to'g'ri yoki noto'g'ri ekani va qisqa izoh chiqadi. "
        "Har bir to'g'ri javob — 1 ball. Maksimal natija — 15 ball."
    )
    await update.effective_message.reply_text(
        text, parse_mode=ParseMode.HTML, reply_markup=start_keyboard()
    )

async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await begin_quiz(update.effective_message, context)

async def begin_quiz(message, context):
    context.user_data["quiz_session"] = {"index": 0, "score": 0, "answers": []}
    await send_question(message, context)

async def send_question(message, context):
    s = session(context)
    if not s:
        await message.reply_text("Avval /start buyrug'i orqali o'yinni boshlang.")
        return
    i = s["index"]
    if i >= len(QUIZ):
        await show_result(message, context)
        return
    q = QUIZ[i]
    text = (
        f"🧠 <b>Savol {i+1}/{len(QUIZ)}</b>\n\n"
        f"{escape(q['q'])}\n\n"
        f"Joriy ball: <b>{s['score']}</b> / {len(QUIZ)}"
    )
    await message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=quiz_keyboard())

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data or ""

    if data == "begin":
        await query.edit_message_reply_markup(reply_markup=None)
        await begin_quiz(query.message, context)
        return

    if data == "share_help":
        bot_username = context.bot.username
        link = f"https://t.me/{bot_username}?start=quiz" if bot_username else ""
        share_text = (
            "📤 <b>O'yinni boshqalarga ulashish</b>\n\n"
            "1. Quyidagi havolani nusxalab Telegram guruh yoki do'stlaringizga yuboring.\n"
            "2. Ular havolani bosib botni ochadi va <b>Start</b> tugmasini bosadi.\n"
            "3. Har bir ishtirokchi o'z natijasini alohida oladi."
        )
        if link:
            share_text += f"\n\n🔗 Bot havolasi: {escape(link)}"
            share_text += (
                "\n\nUlashish uchun tayyor havola:\n"
                f"https://t.me/share/url?url={link}&text=“Mif%20yoki%20haqiqat?”%2015%20savolli%20viktorinani%20sinab%20ko'ring!"
            )
        else:
            share_text += "\n\nBot havolasi bot ishga tushirilgach ko'rinadi."
        await query.message.reply_text(share_text, parse_mode=ParseMode.HTML)
        return

    if data == "finish":
        s = session(context)
        if not s:
            await query.message.reply_text("Hozir faol o'yin yo'q. /start buyrug'ini bosing.")
            return
        await query.edit_message_reply_markup(reply_markup=None)
        await show_result(query.message, context, stopped=True)
        return

    if data.startswith("answer:"):
        s = session(context)
        if not s:
            await query.message.reply_text("O'yin sessiyasi topilmadi. /start buyrug'ini bosing.")
            return
        i = s["index"]
        if i >= len(QUIZ):
            await query.message.reply_text("Bu o'yin yakunlangan. Yangi o'yin uchun /quiz buyrug'ini bosing.")
            return

        chosen = data.split(":", 1)[1]
        q = QUIZ[i]
        correct = chosen == q["a"]
        if correct:
            s["score"] += 1
        s["answers"].append({"chosen": chosen, "correct": q["a"], "ok": correct})
        s["index"] += 1

        result = "✅ <b>To'g'ri!</b>" if correct else "❌ <b>Noto'g'ri.</b>"
        feedback = (
            f"{result}\n"
            f"Sizning javobingiz: <b>{chosen}</b>\n"
            f"To'g'ri javob: <b>{q['a']}</b>\n\n"
            f"💡 {escape(q['why'])}\n\n"
            f"📊 Joriy ball: <b>{s['score']}/{len(QUIZ)}</b>"
        )
        next_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "🏁 Natijani ko'rish" if s["index"] >= len(QUIZ) else "➡️ Keyingi savol",
                callback_data="next"
            )]
        ])
        await query.edit_message_text(feedback, parse_mode=ParseMode.HTML, reply_markup=next_markup)
        return

    if data == "next":
        await query.edit_message_reply_markup(reply_markup=None)
        await send_question(query.message, context)

async def show_result(message, context, stopped=False):
    s = session(context)
    if not s:
        await message.reply_text("Natija topilmadi. /start buyrug'ini bosing.")
        return
    answered = len(s["answers"])
    score = s["score"]
    percent = round(score / len(QUIZ) * 100)
    if answered == 0:
        evaluation = "Hali savollarga javob berilmadi. Yana urinib ko'ring!"
    elif score >= 13:
        evaluation = "A'lo! Mavzuni juda yaxshi o'zlashtirgansiz. 🌟"
    elif score >= 10:
        evaluation = "Yaxshi natija! Ayrim mavzularni yana takrorlang. 👏"
    elif score >= 7:
        evaluation = "Qoniqarli. Javoblar izohlarini qayta ko'rib chiqing. 📚"
    else:
        evaluation = "Mavzuni yana takrorlash foydali bo'ladi. 💪"

    title = "🏁 <b>O'yin yakunlandi!</b>" if not stopped else "⏹ <b>O'yin muddatidan oldin tugatildi.</b>"
    text = (
        f"{title}\n\n"
        f"✅ To'g'ri javoblar: <b>{score}</b>\n"
        f"❌ Noto'g'ri javoblar: <b>{answered-score}</b>\n"
        f"📝 Javob berilgan savollar: <b>{answered}/{len(QUIZ)}</b>\n"
        f"🎯 Natija: <b>{percent}%</b>\n\n"
        f"{evaluation}\n\n"
        "Yangi urinish uchun quyidagi tugmani bosing yoki /quiz buyrug'ini yuboring."
    )
    await message.reply_text(
        text, parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Qayta o'ynash", callback_data="begin")],
            [InlineKeyboardButton("📤 O'yinni ulashish", callback_data="share_help")],
        ])
    )
    context.user_data.pop("quiz_session", None)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Buyruqlar:\n"
        "/start — botni ochish\n"
        "/quiz — yangi o'yin boshlash\n"
        "/share — o'yin havolasini ulashish yo'riqnomasi\n"
        "/help — yordam"
    )

async def share_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = context.bot.username
    if not bot_username:
        await update.effective_message.reply_text("Bot username'i aniqlanmadi. Keyinroq urinib ko'ring.")
        return
    link = f"https://t.me/{bot_username}?start=quiz"
    text = (
        "📤 “Mif yoki haqiqat?” viktorinasini ulashing!\n\n"
        f"Bot havolasi: {link}\n\n"
        "Havolani do'stlaringizga yoki Telegram guruhiga yuboring. Har bir ishtirokchi o'z ballini oladi."
    )
    share_url = f"https://t.me/share/url?url={link}&text=Mif%20yoki%20haqiqat%2015%20savolli%20viktorina"
    await update.effective_message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📨 Telegram orqali ulashish", url=share_url)],
            [InlineKeyboardButton("🎮 O'yinni boshlash", callback_data="begin")],
        ])
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("share", share_command))
    app.add_handler(CallbackQueryHandler(on_button))
    log.info("Bot ishga tushmoqda...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
