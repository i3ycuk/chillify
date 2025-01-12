from brain import load_dotenv, os

load_dotenv()

# Основные настройки
API_TOKEN = os.getenv("API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

DB_SETTINGS = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT")
}

missing_vars = []
required_vars = {
    "API_TOKEN": API_TOKEN,
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "GIPHY_API_KEY": GIPHY_API_KEY,
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "DB_NAME": DB_SETTINGS.get('dbname'),
    "DB_USER": DB_SETTINGS.get('user'),
    "DB_PASSWORD": DB_SETTINGS.get('password'),
    "DB_HOST": DB_SETTINGS.get('host'),
    "DB_PORT": DB_SETTINGS.get('port')
}

for var_name, var_value in required_vars.items():
    if not var_value:
        missing_vars.append(var_name)

if missing_vars:
    raise ValueError(f"Не установлены следующие переменные окружения: {', '.join(missing_vars)}")

# Настройки кэша
CACHE_CLEANUP_INTERVAL = 24 * 60 * 60  # Очистка кэша (24 часа)

# Параметры запуска
APP_NAME = "Chillify 🌿"
APP_VERSION = "1.0"
DEBUG = True
SESSION_NAME = "chillify_client"