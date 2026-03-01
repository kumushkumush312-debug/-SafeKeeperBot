from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from typing import Any

async def handle(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tekshirish tugmasi bosilganda"""
    await query.edit_message_text(
        "🛡️ **TEKSHIRISH BO'LIMI**\n\n"
        "Menga fayl, video yoki rasm yuboring, men virusga tekshirib beraman."
    )

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tekshirish komandasi"""
    await update.message.reply_text(
        "🛡️ Menga fayl yuboring, men tekshirib beraman."
    )