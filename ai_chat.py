from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from typing import Any

async def handle(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE) -> None:
    """AI suhbat tugmasi bosilganda"""
    await query.edit_message_text(
        "🤖 **AI SUHBAT**\n\n"
        "Menga savolingizni yozing, men javob beraman."
    )

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """AI suhbat komandasi"""
    await update.message.reply_text(
        "🤖 AI suhbat rejimi faollashtirildi. Savolingizni yozing."
    )