import logging
import os
import tempfile
from typing import Optional, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from config import BOT_TOKEN, ADMIN_ID
from database import Database
from virus_scanner import VirusScanner
import handlers.start as start_handler
import handlers.check as check_handler
import handlers.game as game_handler
import handlers.ai_chat as ai_handler
import handlers.group as group_handler
import handlers.exit as exit_handler

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global obyektlar
db = Database()
scanner = VirusScanner()


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE) -> None:  # TO'G'RI: context qo'shildi va return type None
    """Start buyrug'i - asosiy menyu"""
    user = update.effective_user

    if user is None:
        return

    # Foydalanuvchi bloklanganligini tekshirish
    if db.is_user_blocked(user.id):
        await update.message.reply_text("🚫 Siz bloklangansiz! 7 kundan keyin qayta urinib ko'ring.")
        return

    # Asosiy menyu tugmalari
    keyboard = [
        [InlineKeyboardButton("🛡️ Tekshirish", callback_data='check')],
        [InlineKeyboardButton("🎮 O'yin", callback_data='game')],
        [InlineKeyboardButton("🤖 AI Suhbat", callback_data='ai')],
        [InlineKeyboardButton("👥 Guruhga qo'shish", callback_data='group')],
        [InlineKeyboardButton("🚪 Chiqish", callback_data='exit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\n\n"
        "🛡️ Himoyachi botga xush kelibsiz!\n"
        "Men sizni virusli fayllardan himoya qilaman.\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=reply_markup
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fayl kelganda tekshirish"""
    user = update.effective_user

    if user is None:
        return

    if db.is_user_blocked(user.id):
        await update.message.reply_text("🚫 Siz bloklangansiz!")
        return

    file = await update.message.document.get_file()

    with tempfile.NamedTemporaryFile(delete=False, suffix=update.message.document.file_name) as tmp_file:
        await file.download_to_drive(tmp_file.name)
        scan_result = await scanner.scan_file(tmp_file.name)

        if scan_result['is_infected']:
            db.block_user(
                user.id,
                user.username,
                user.first_name,
                f"Virus: {scan_result.get('virus_name', 'Noma`lum')}"
            )

            await context.bot.send_message(
                ADMIN_ID,
                f"🚨 Virus aniqlandi!\n"
                f"Foydalanuvchi: {user.first_name} (@{user.username})\n"
                f"ID: {user.id}\n"
                f"Fayl: {update.message.document.file_name}\n"
                f"Virus: {scan_result.get('virus_name', 'Noma`lum')}\n"
                f"Holat: 7 kunga bloklandi"
            )

            await update.message.reply_text(
                "🚫 SIZ BLOKLANDINGIZ!\n\n"
                "Sabab: Virusli fayl yubordingiz.\n"
                "Bloklash muddati: 7 kun"
            )

            logger.info(f"User {user.id} blocked for sending virus file")
        else:
            await update.message.reply_text("✅ Fayl virusdan toza!")
            db.add_scan_log(
                file.file_id,
                update.message.document.file_name,
                user.id,
                "clean"
            )

    os.unlink(tmp_file.name)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tugmalar bosilganda ishlaydi"""
    query = update.callback_query
    await query.answer()

    if query.data == 'check':
        await check_handler.handle(query, context)
    elif query.data == 'game':
        await game_handler.handle(query, context)
    elif query.data == 'ai':
        await ai_handler.handle(query, context)
    elif query.data == 'group':
        await group_handler.handle(query, context)
    elif query.data == 'exit':
        await exit_handler.handle(query, context)


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Video kelganda tekshirish"""
    await handle_document(update, context)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Rasm kelganda tekshirish"""
    user = update.effective_user

    if user is None:
        return

    if db.is_user_blocked(user.id):
        await update.message.reply_text("🚫 Siz bloklangansiz!")
        return

    file = await update.message.photo[-1].get_file()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        await file.download_to_drive(tmp_file.name)
        scan_result = await scanner.scan_file(tmp_file.name)

        if scan_result['is_infected']:
            db.block_user(user.id, user.username, user.first_name, "Virusli rasm")
            await context.bot.send_message(
                ADMIN_ID,
                f"🚨 Virusli rasm!\nFoydalanuvchi: {user.first_name} (@{user.username})\nID: {user.id}"
            )
            await update.message.reply_text("🚫 Siz bloklandingiz! Virusli rasm yubordingiz.")
        else:
            await update.message.reply_text("✅ Rasm xavfsiz!")

    os.unlink(tmp_file.name)


def main() -> None:
    """Botni ishga tushirish"""
    # Bot yaratish
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tekshirish", check_handler.command))
    application.add_handler(CommandHandler("oyin", game_handler.command))
    application.add_handler(CommandHandler("ai", ai_handler.command))
    application.add_handler(CommandHandler("guruhga_qoshish", group_handler.command))
    application.add_handler(CommandHandler("chiqish", exit_handler.command))

    # Fayl handlerlari
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Tugmalar uchun handler
    application.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()