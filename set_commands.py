import asyncio
from telegram import Bot, BotCommand
from config import BOT_TOKEN


async def set_commands():
    bot = Bot(token=BOT_TOKEN)

    commands = [
        BotCommand("start", "Botni ishga tushirish"),
        BotCommand("tekshirish", "Faylni virusga tekshirish"),
        BotCommand("oyin", "Son topish o'yini"),
        BotCommand("ai", "AI bilan suhbat"),
        BotCommand("guruhga_qoshish", "Botni guruhga qo'shish"),
        BotCommand("chiqish", "Botdan chiqish"),
    ]

    await bot.set_my_commands(commands)
    print("✅ Komandalar o'rnatildi!")


if __name__ == "__main__":
    asyncio.run(set_commands())