from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import pytz
from config import TIMEZONE, MIN_MESSAGES_FOR_ANALYSIS
from database import (
    register_user,
    save_message,
    get_user_messages,
    get_message_count,
    clear_user_data,
    save_report
)
from sentiment import get_sentiment
from reporter import generate_and_save_report

tz = pytz.timezone(TIMEZONE)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await register_user(user.id, user.username or user.first_name)
    
    await update.message.reply_text(
        "i'm here.\n\n"
        "talk. rant. vent. say whatever you want.\n"
        "i won't reply. i won't judge. i'm just watching.\n\n"
        "every week i'll tell you what i found.\n"
        "every month, the full picture.\n\n"
        "go ahead."
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    
    if not message or not message.text:
        return
    
    content = message.text
    now = datetime.now(tz)
    hour = now.hour
    day_of_week = now.weekday()
    
    await save_message(user.id, content, hour, day_of_week)
    
    sentiment_result = get_sentiment(content)
    score = sentiment_result['score']
    
    count = await get_message_count(user.id)
    
    if count % 25 == 0:
        await update.message.reply_text("still here.")


async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    count = await get_message_count(user.id)
    
    if count < MIN_MESSAGES_FOR_ANALYSIS:
        await update.message.reply_text(
            f"you've sent {count} messages.\n"
            f"i need at least {MIN_MESSAGES_FOR_ANALYSIS} to see anything real.\n"
            "keep going."
        )
        return
    
    await update.message.reply_text("running your profile. give me a second.")
    
    messages = await get_user_messages(user.id, days=30)
    
    report = await generate_and_save_report(
        user_id=user.id,
        messages=messages,
        report_type="manual",
        save_func=save_report
    )
    
    await update.message.reply_text(report)


async def clear_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await clear_user_data(user.id)
    await update.message.reply_text(
        "done. everything's gone.\n"
        "we start from zero."
    )