from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from typing import Any

async def handle(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Chiqish tugmasi bosilganda"""
    await query.edit_message_text(
        "🚪 **CHIQISH**\n\n"
        "Botdan chiqdingiz. Qaytish uchun /start ni bosing."
    )

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Chiqish komandasi"""
    await update.message.reply_text(
        "🚪 Xayr! Qaytish uchun /start ni bosing."
    )