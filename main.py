import os
import random
import logging
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))
app = Flask(__name__)

@app.get("/")
def health():
    return "Senesh A/L MCQ Bot is running."

# Starter questions are examples. Add verified syllabus/past-paper questions here.
QUESTIONS = [
    {
        "subject": "Combined Maths",
        "si": "x² - 5x + 6 = 0 නම් x හි අගයන් මොනවාද?",
        "en": "If x² - 5x + 6 = 0, what are the values of x?",
        "options_si": ["1 සහ 6", "2 සහ 3", "-2 සහ -3", "1 සහ 5"],
        "options_en": ["1 and 6", "2 and 3", "-2 and -3", "1 and 5"],
        "answer": 1,
        "explain_si": "x² - 5x + 6 = (x - 2)(x - 3), එබැවින් x = 2 හෝ 3.",
        "explain_en": "Factorising gives (x - 2)(x - 3) = 0, so x = 2 or 3."
    },
    {
        "subject": "Combined Maths",
        "si": "sin 30° හි අගය කීයද?",
        "en": "What is the value of sin 30°?",
        "options_si": ["0", "1/2", "√3/2", "1"],
        "options_en": ["0", "1/2", "√3/2", "1"],
        "answer": 1,
        "explain_si": "sin 30° = 1/2.",
        "explain_en": "sin 30° = 1/2."
    },
    {
        "subject": "Physics",
        "si": "වේගයේ SI ඒකකය කුමක්ද?",
        "en": "What is the SI unit of speed?",
        "options_si": ["m", "m/s", "m/s²", "kg"],
        "options_en": ["m", "m/s", "m/s²", "kg"],
        "answer": 1,
        "explain_si": "වේගයේ SI ඒකකය මීටර් තත්පරයට (m/s) වේ.",
        "explain_en": "The SI unit of speed is metres per second (m/s)."
    },
    {
        "subject": "Chemistry",
        "si": "ජලයේ රසායනික සූත්‍රය කුමක්ද?",
        "en": "What is the chemical formula of water?",
        "options_si": ["CO₂", "O₂", "H₂O", "NaCl"],
        "options_en": ["CO₂", "O₂", "H₂O", "NaCl"],
        "answer": 2,
        "explain_si": "ජලයේ රසායනික සූත්‍රය H₂O වේ.",
        "explain_en": "The chemical formula of water is H₂O."
    },
    {
        "subject": "Biology",
        "si": "ප්‍රභාසංශ්ලේෂණයට අවශ්‍ය වර්ණකය කුමක්ද?",
        "en": "Which pigment is required for photosynthesis?",
        "options_si": ["හීමොග්ලොබින්", "ක්ලෝරෝෆිල්", "මෙලනින්", "ඉන්සියුලින්"],
        "options_en": ["Haemoglobin", "Chlorophyll", "Melanin", "Insulin"],
        "answer": 1,
        "explain_si": "ක්ලෝරෝෆිල් ආලෝක ශක්තිය අවශෝෂණය කරයි.",
        "explain_en": "Chlorophyll absorbs light energy."
    },
    {
        "subject": "ICT",
        "si": "CPU යන්නෙහි සම්පූර්ණ නම කුමක්ද?",
        "en": "What does CPU stand for?",
        "options_si": ["Central Processing Unit", "Computer Personal Unit", "Control Program Utility", "Central Power User"],
        "options_en": ["Central Processing Unit", "Computer Personal Unit", "Control Program Utility", "Central Power User"],
        "answer": 0,
        "explain_si": "CPU යනු Central Processing Unit යන්නයි.",
        "explain_en": "CPU stands for Central Processing Unit."
    }
]

SUBJECTS = [
    ("maths", "Combined Maths"),
    ("physics", "Physics"),
    ("chemistry", "Chemistry"),
    ("biology", "Biology"),
    ("ict", "ICT"),
    ("all", "All subjects"),
]
SUBJECT_ALIASES = {
    "maths": "Combined Maths", "physics": "Physics",
    "chemistry": "Chemistry", "biology": "Biology",
    "ict": "ICT", "all": "All subjects"
}

def lang(context):
    return context.user_data.get("lang", "si")

def tr(context, si, en):
    return si if lang(context) == "si" else en

def subject_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Combined Maths", callback_data="sub:maths"),
         InlineKeyboardButton("Physics", callback_data="sub:physics")],
        [InlineKeyboardButton("Chemistry", callback_data="sub:chemistry"),
         InlineKeyboardButton("Biology", callback_data="sub:biology")],
        [InlineKeyboardButton("ICT", callback_data="sub:ict"),
         InlineKeyboardButton("All subjects", callback_data="sub:all")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇱🇰 සිංහල", callback_data="lang:si"),
         InlineKeyboardButton("🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton("🎯 MCQ Target", callback_data="mode:target"),
         InlineKeyboardButton("📚 Past Paper MCQ", callback_data="mode:past")]
    ])
    await update.effective_message.reply_text(
        "🎓 Senesh A/L MCQ Target Bot\n\n"
        "භාෂාව තෝරන්න / Choose your language:",
        reply_markup=keyboard
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "/start - Main menu\n/mcq - Start an MCQ\n/target - MCQ Target\n/pastpaper - Past Paper MCQ\n/score - View your score\n/subjects - Choose a subject\n/language - Change language"
    )

async def language_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("🇱🇰 සිංහල", callback_data="lang:si"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang:en")
    ]])
    await update.effective_message.reply_text("Choose language / භාෂාව තෝරන්න:", reply_markup=keyboard)

async def subjects_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Choose a subject / විෂය තෝරන්න:", reply_markup=subject_keyboard())

async def target_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "target"
    await update.effective_message.reply_text(
        tr(context, "🎯 MCQ Target සඳහා විෂය තෝරන්න:", "Choose a subject for MCQ Target:"),
        reply_markup=subject_keyboard()
    )

async def past_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "past"
    await update.effective_message.reply_text(
        tr(context, "📚 Past Paper MCQ සඳහා විෂය තෝරන්න:", "Choose a subject for Past Paper MCQ:"),
        reply_markup=subject_keyboard()
    )

async def mcq_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.setdefault("mode", "target")
    await update.effective_message.reply_text(
        tr(context, "ප්‍රශ්න සඳහා විෂය තෝරන්න:", "Choose a subject:"),
        reply_markup=subject_keyboard()
    )

async def send_question(query, context, subject_key):
    subject = SUBJECT_ALIASES.get(subject_key, "All subjects")
    mode = context.user_data.get("mode", "target")
    available = QUESTIONS if subject == "All subjects" else [
        q for q in QUESTIONS if q["subject"] == subject
    ]
    if not available:
        await query.edit_message_text(
            tr(context, "මේ විෂයට තවම ප්‍රශ්න එකතු කර නැහැ.", "No questions have been added for this subject yet.")
        )
        return
    q = random.choice(available)
    context.user_data["current_question"] = q
    context.user_data["current_subject"] = subject_key
    options = q["options_si"] if lang(context) == "si" else q["options_en"]
    keyboard = [[InlineKeyboardButton(f"{'ABCD'[i]}. {opt}", callback_data=f"answer:{i}")]
                for i, opt in enumerate(options)]
    keyboard.append([InlineKeyboardButton(
        tr(context, "➡️ ඊළඟ ප්‍රශ්නය", "➡️ Next question"), callback_data=f"next:{subject_key}"
    )])
    mode_label = tr(context, "🎯 MCQ Target", "🎯 MCQ Target") if mode == "target" else tr(context, "📚 Past Paper MCQ", "📚 Past Paper MCQ")
    await query.edit_message_text(
        f"{mode_label}\n📘 {q['subject']}\n\n{q[lang(context)]}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lang:"):
        context.user_data["lang"] = data.split(":")[1]
        await query.edit_message_text(
            tr(context, "✅ භාෂාව සිංහල ලෙස සකස් කළා.\n/start භාවිතයෙන් menu එකට යන්න.", "✅ Language set to English.\nUse /start to open the menu.")
        )
        return

    if data.startswith("mode:"):
        context.user_data["mode"] = data.split(":")[1]
        await query.edit_message_text(
            tr(context, "විෂය තෝරන්න:", "Choose a subject:"),
            reply_markup=subject_keyboard()
        )
        return

    if data.startswith("sub:"):
        await send_question(query, context, data.split(":")[1])
        return

    if data.startswith("next:"):
        await send_question(query, context, data.split(":")[1])
        return

    if data.startswith("answer:"):
        q = context.user_data.get("current_question")
        if not q:
            await query.edit_message_text(tr(context, "අලුත් ප්‍රශ්නයක් සඳහා /mcq භාවිතා කරන්න.", "Use /mcq to get a question."))
            return
        selected = int(data.split(":")[1])
        correct = q["answer"]
        score = context.user_data.setdefault("score", {"right": 0, "total": 0})
        score["total"] += 1
        if selected == correct:
            score["right"] += 1
            result = tr(context, "✅ නිවැරදියි!", "✅ Correct!")
        else:
            options = q["options_si"] if lang(context) == "si" else q["options_en"]
            result = tr(context, "❌ වැරදියි!", "❌ Incorrect!") + f"\n{tr(context, 'නිවැරදි පිළිතුර', 'Correct answer')}: {'ABCD'[correct]}. {options[correct]}"
        explanation = q["explain_si"] if lang(context) == "si" else q["explain_en"]
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(tr(context, "ඊළඟ ප්‍රශ්නය", "Next question"), callback_data=f"next:{context.user_data.get('current_subject', 'all')}")],
            [InlineKeyboardButton(tr(context, "ලකුණු", "My score"), callback_data="score")]
        ])
        await query.edit_message_text(f"{result}\n\n💡 {explanation}", reply_markup=keyboard)
        context.user_data.pop("current_question", None)
        return

    if data == "score":
        score = context.user_data.get("score", {"right": 0, "total": 0})
        await query.edit_message_text(
            tr(context, f"📊 ලකුණු: {score['right']} / {score['total']}", f"📊 Score: {score['right']} / {score['total']}")
        )

async def score_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score = context.user_data.get("score", {"right": 0, "total": 0})
    await update.effective_message.reply_text(
        tr(context, f"📊 ඔබේ ලකුණු: {score['right']} / {score['total']}", f"📊 Your score: {score['right']} / {score['total']}")
    )

def main():
    if not TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable.")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("language", language_cmd))
    application.add_handler(CommandHandler("subjects", subjects_cmd))
    application.add_handler(CommandHandler("target", target_cmd))
    application.add_handler(CommandHandler("pastpaper", past_cmd))
    application.add_handler(CommandHandler("mcq", mcq_cmd))
    application.add_handler(CommandHandler("score", score_cmd))
    application.add_handler(CallbackQueryHandler(callbacks))
    application.run_polling()

if __name__ == "__main__":
    # Start Telegram polling in a background thread while Flask serves Render's health check.
    import threading
    threading.Thread(target=main, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
