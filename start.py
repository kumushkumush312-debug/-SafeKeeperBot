from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from typing import Any

async def handle(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start tugmasi bosilganda"""
    await query.edit_message_text(
        "Siz allaqachon boshlagansiz! /start ni bosing.\n\n"
        "Asosiy menyuga qaytish uchun /start buyrug'ini yuboring."
    )

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start komandasi"""
    # Bu funksiya kerak bo'lsa ishlatiladi
    pass