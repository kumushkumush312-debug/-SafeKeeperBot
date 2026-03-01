from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from typing import Any

async def handle(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guruh tugmasi bosilganda"""
    await query.edit_message_text(
        "👥 **GURUHGA QO'SHISH**\n\n"
        "Botni guruhingizga qo'shish uchun admin qiling."
    )

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guruh komandasi"""
    await update.message.reply_text(
        "👥 Meni guruhingizga qo'shish uchun:\n"
        "1. Guruhga qo'shing\n"
        "2. Admin qiling"
    )