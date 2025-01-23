import socket
import threading
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram-клиент")
        self.setGeometry(100, 100, 800, 600)

        # Основной layout
        layout = QVBoxLayout()

        # Поле для сообщений
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)

        # Поле для ввода сообщения
        self.message_input = QLineEdit()

        # Кнопка отправки
        self.send_button = QPushButton("Отправить")

        layout.addWidget(self.message_display)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

        # Устанавливаем layout для окна
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Запуск сервера IPC
        self.start_ipc_server()

    def start_ipc_server(self):
        """Запуск сервера IPC для получения сообщений от бота."""
        def ipc_server():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", 65432))
                s.listen()
                while True:
                    conn, addr = s.accept()
                    with conn:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            message = data.decode()
                            self.message_display.append(message)  # Отображаем сообщение в интерфейсе

        # Запуск сервера в отдельном потоке
        threading.Thread(target=ipc_server, daemon=True).start()