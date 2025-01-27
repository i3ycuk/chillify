from pathlib import Path
import sys

# Добавляем корень проекта в sys.path
project_root = Path(__file__).resolve().parent.parent  # Переход на два уровня вверх
sys.path.append(str(project_root))

from brain import client, TelegramClient, events, QApplication, logging, subprocess, API_TOKEN


# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    await client.start(API_TOKEN)
    me = await client.get_me()
    logger.info(f'Авторизация как: @{me.username}')

    # Запуск бота через subprocess
    try:
        subprocess.Popen([sys.executable, "bot/main.py"])
        logger.info("Клиент успешно запущен.")
    except Exception as e:
        logger.error(f"Ошибка при запуске клиента: {e}")

with client:
    client.loop.run_until_complete(main())
