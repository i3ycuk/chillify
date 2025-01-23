import socket
import logging

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class IPCClient:
    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Подключение к серверу."""
        try:
            self.socket.connect((self.host, self.port))
            logger.info("Успешно подключен к серверу IPC.")
        except Exception as e:
            logger.error(f"Ошибка при подключении к серверу IPC: {e}")

    def send_message(self, message):
        """Отправка сообщения на сервер."""
        try:
            self.socket.sendall(message.encode())
            logger.debug(f"Сообщение отправлено: {message}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")

    def close(self):
        """Закрытие соединения."""
        self.socket.close()
        logger.info("Соединение с сервером IPC закрыто.")