@echo off
cd C:\Users\AliCom-1\PycharmProjects\kim

echo handlers papkasi yaratilmoqda...
if not exist handlers mkdir handlers

echo __init__.py yaratilmoqda...
echo. > handlers\__init__.py

echo start.py yaratilmoqda...
echo from telegram import Update > handlers\start.py
echo from telegram.ext import ContextTypes >> handlers\start.py
echo. >> handlers\start.py
echo async def handle(query, context: ContextTypes.DEFAULT_TYPE): >> handlers\start.py
echo     await query.edit_message_text( >> handlers\start.py
echo         "Siz allaqachon boshlagansiz! /start ni bosing." >> handlers\start.py
echo     ) >> handlers\start.py
echo. >> handlers\start.py
echo async def command(update: Update, context: ContextTypes.DEFAULT_TYPE): >> handlers\start.py
echo     pass >> handlers\start.py

echo check.py yaratilmoqda...
echo from telegram import Update > handlers\check.py
echo from telegram.ext import ContextTypes >> handlers\check.py
echo. >> handlers\check.py
echo async def handle(query, context: ContextTypes.DEFAULT_TYPE): >> handlers\check.py
echo     await query.edit_message_text("🛡️ Tekshirish bo'limi") >> handlers\check.py
echo. >> handlers\check.py
echo async def command(update: Update, context: ContextTypes.DEFAULT_TYPE): >> handlers\check.py
echo     await update.message.reply_text("🛡️ Fayl yuboring") >> handlers\check.py

echo game.py yaratilmoqda...
echo from telegram import Update > handlers\game.py
echo from telegram.ext import ContextTypes >> handlers\game.py
echo import random >> handlers\game.py
echo. >> handlers\game.py
echo async def handle(query, context: ContextTypes.DEFAULT_TYPE): >> handlers\game.py
echo     await query.edit_message_text("🎮 O'yin bo'limi") >> handlers\game.py
echo. >> handlers\game.py
echo async def command(update: Update, context: ContextTypes.DEFAULT_TYPE): >> handlers\game.py
echo     await update.message.reply_text("🎮 O'yin boshlandi") >> handlers\game.py

echo ai_chat.py yaratilmoqda...
echo from telegram import Update > handlers\ai_chat.py
echo from telegram.ext import ContextTypes >> handlers\ai_chat.py
echo. >> handlers\ai_chat.py
echo async def handle(query, context: ContextTypes.DEFAULT_TYPE): >> handlers\ai_chat.py
echo     await query.edit_message_text("🤖 AI Suhbat") >> handlers\ai_chat.py
echo. >> handlers\ai_chat.py
echo async def command(update: Update, context: ContextTypes.DEFAULT_TYPE): >> handlers\ai_chat.py
echo     await update.message.reply_text("🤖 AI rejimi") >> handlers\ai_chat.py

echo group.py yaratilmoqda...
echo from telegram import Update > handlers\group.py
echo from telegram.ext import ContextTypes >> handlers\group.py
echo. >> handlers\group.py
echo async def handle(query, context: ContextTypes.DEFAULT_TYPE): >> handlers\group.py
echo     await query.edit_message_text("👥 Guruhga qo'shish") >> handlers\group.py
echo. >> handlers\group.py
echo async def command(update: Update, context: ContextTypes.DEFAULT_TYPE): >> handlers\group.py
echo     await update.message.reply_text("👥 Guruhga qo'shing") >> handlers\group.py

echo exit.py yaratilmoqda...
echo from telegram import Update > handlers\exit.py
echo from telegram.ext import ContextTypes >> handlers\exit.py
echo. >> handlers\exit.py
echo async def handle(query, context: ContextTypes.DEFAULT_TYPE): >> handlers\exit.py
echo     await query.edit_message_text("🚪 Chiqish") >> handlers\exit.py
echo. >> handlers\exit.py
echo async def command(update: Update, context: ContextTypes.DEFAULT_TYPE): >> handlers\exit.py
echo     await update.message.reply_text("🚪 Xayr!") >> handlers\exit.py

echo Bajarildi!
pause