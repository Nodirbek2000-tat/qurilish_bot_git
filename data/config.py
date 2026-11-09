from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot tokeni (@BotFather)
API_URL = env.str("API_URL", "http://127.0.0.1:8001").rstrip("/")  # sayt backendi (Django)
BOT_API_KEY = env.str("BOT_API_KEY")  # qurilish/.env dagi BOT_API_KEY bilan bir xil
