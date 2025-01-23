from pathlib import Path
import sys

# Добавляем корень проекта в sys.path
project_root = Path(__file__).resolve().parent.parent  # Переход на два уровня вверх
sys.path.append(str(project_root))

import subprocess
import logging
from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow  # Импортируем главное окно
from brain import client
from telethon import TelegramClient, events
from client.backend.ipc import IPCClient  # Импортируем IPCClient

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Инициализация IPCClient
ipc_client = IPCClient()
ipc_client.connect()

def main():
    # Запуск графического интерфейса
    app = QApplication(sys.argv)

    # Создаем и показываем главное окно
    window = MainWindow()
    window.show()

    # Запуск бота через subprocess
    try:
        subprocess.Popen([sys.executable, "bot/main.py"])
        logger.info("Клиент успешно запущен.")
    except Exception as e:
        logger.error(f"Ошибка при запуске клиента: {e}")

    sys.exit(app.exec_())


@client.on(events.NewMessage)
async def handle_message(event):
    """Обработка новых сообщений."""
    user = await event.get_sender()
    text = event.text
    logger.info(f"Новое сообщение от {user.username}: {text}")

    # Отправляем сообщение в интерфейс через IPC
    ipc_client.send_message(f"{user.username}: {text}")

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
    main()