from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
import random
from typing import Any


async def handle(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE) -> None:
    """O'yin tugmasi bosilganda"""
    await query.edit_message_text(
        "🎮 **O'YINLAR**\n\n"
        "Son topish o'yini: 1-10 oralig'ida son o'yladim. Toping!"
    )

    number = random.randint(1, 10)
    context.user_data['game_number'] = number
    context.user_data['game_active'] = True


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """O'yin komandasi"""
    await update.message.reply_text(
        "🎮 Son topish o'yini boshlandi! Men son o'yladim (1-10)."
    )