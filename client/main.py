from pathlib import Path
import sys

# Добавляем корень проекта в sys.path
project_root = Path(__file__).resolve().parent.parent  # Переход на два уровня вверх
sys.path.append(str(project_root))

import subprocess
import logging
from PyQt5.QtWidgets import QApplication
from brain import client
from telethon import TelegramClient, events


# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():

    # Запуск бота через subprocess
    try:
        subprocess.Popen([sys.executable, "bot/main.py"])
        logger.info("Клиент успешно запущен.")
    except Exception as e:
        logger.error(f"Ошибка при запуске клиента: {e}")

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
    main()