import os
from dotenv import load_dotenv

load_dotenv()

# Bot tokenini .env faylidan o'qish
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Admin ID (bot egasi)
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

# Virus tekshirish sozlamalari
CLAMAV_HOST = "localhost"
CLAMAV_PORT = 3310

# Ma'lumotlar bazasi
DATABASE_PATH = "bot_database.db"

# Bloklash muddati (kun)
BLOCK_DAYS = 7