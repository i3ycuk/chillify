from pathlib import Path
import sys

# Добавляем корень проекта в sys.path
project_root = Path(__file__).resolve().parent.parent  # Переход на два уровня вверх
sys.path.append(str(project_root))

# Теперь можно импортировать brain.py
from brain import logging, sys, asyncio, TelegramClient, events, StringSession, API_ID, API_HASH, PHONE_NUMBER, LOG_FILE, LOG_LEVEL, create_cache_table, cleanup_cache, store_message_data, get_message_data, delete_message_data, QtWidgets, uic, QMessageBox, QPlainTextEdit, QPushButton, QLineEdit, os, errors, importlib, QListWidget, json, utils, QListWidgetItem, dp, UpdateStatusRequest, QLabel, QTimer, telethon

print(telethon.__version__)
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

client = TelegramClient('session_name', API_ID, API_HASH)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Вызов конструктора суперкласса
        print("MainWindow.__init__ start")  # Отладочный вывод
        super().__init__()
        print("super().__init__() done")  # Отладочный вывод
        try:
            # Загружаем интерфейс
            uic.loadUi('client/ui/mainwindow.ui', self)
            print("uic.loadUi() done")
        except Exception as e:
            print(f"Error loading UI: {e}") # Отладочный вывод
            return # Важно! Выходим из __init__ при ошибке

        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #202125; /* Темный фон */
                color: #e0e0e0; /* Светлый текст */
                border: 1px solid #303136; /* Темная рамка */
                padding: 5px;
            }
            QLineEdit {
                background-color: #202125;
                color: #e0e0e0;
                border: 1px solid #303136;
                padding: 5px;
            }
            QListWidget {
                background-color: #202125;
                color: #e0e0e0;
                border: none; /* Убираем рамку списка */
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #38393e; /* Цвет выделения */
            }
            QPushButton {
                background-color: #303136;
                color: #e0e0e0;
                border: 1px solid #404146;
                padding: 5px 10px;
                border-radius: 3px; /* Закругленные углы */
            }
            QPushButton:hover {
                background-color: #38393e; /* Цвет при наведении */
            }
            QLabel {
                color: #e0e0e0;
            }
            QFrame {
                background-color: #28292e; /* Фон для фреймов ввода/ответа */
                border: 1px solid #303136;
                margin-top: 5px;
                margin-bottom: 5px;
            }
        """)

    def add_log_message(self, message):
        self.log_widget.appendPlainText(message + "\n")
        self.log_widget.verticalScrollBar().setValue(self.log_widget.verticalScrollBar().maximum())

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    def message_selected(self, item):
        try:
            message_data = json.loads(item.data(Qt.UserRole))
            self.selected_message_id = message_data['id']
        except Exception as e:
            logging.error(f"Error parsing message data: {e}")
            self.show_message("Error", str(e), QMessageBox.Critical)

    async def display_message(self, message):
        try:
            sender = await client.get_entity(message.sender_id)
            sender_name = utils.get_display_name(sender)
            message_text = message.text

            message_data = {'id': message.id, 'chat_id': message.chat_id}
            item_text = f"{sender_name}: {message_text}"

            if message.id in self.message_items:
                # Обновляем существующий элемент
                item = self.message_items[message.id]
                item.setText(item_text)
                item.setData(Qt.UserRole, json.dumps(message_data))
            else:
                # Создаем новый элемент
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, json.dumps(message_data))
                self.messages_list.addItem(item)
                self.message_items[message.id] = item

        except Exception as e:
            logging.error(f"Error display message: {e}")
            self.show_message("Error", str(e), QMessageBox.Critical)

    async def remove_message_from_list(self, message_id):
        if message_id in self.message_items:
            item = self.message_items.pop(message_id)
            self.messages_list.takeItem(self.messages_list.row(item))

    async def clear_chat(self):
        self.messages_list.clear() # Очищаем список виджетов
        self.message_items.clear() # Очищаем словарь

    async def send_reply(self):
        if self.selected_message_id:
            try:
                reply_text = self.reply_input.toPlainText()
                if reply_text:
                    await client.send_message(entity=self.selected_message_id, message=reply_text) # Отвечаем на сообщение
                    self.reply_input.clear()
            except Exception as e:
                self.show_message("Error", str(e), QMessageBox.Critical)
        else:
            self.show_message("Предупреждение", "Выберите сообщение для ответа.", QMessageBox.Warning)

    async def start_client_async(self):
        global client
        if self.bot_task is None:
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    await client.send_code_request(PHONE_NUMBER)
                    try:
                        await client.sign_in(PHONE_NUMBER, input('Enter the code: '))
                    except errors.SessionPasswordNeededError:
                        password = input('Two-step verification enabled. Please enter your password: ')
                        await client.sign_in(password=password)

                base_dir = os.path.dirname(os.path.abspath(__file__))
                handlers_path = os.path.join(base_dir, "handlers")
                if os.path.exists(handlers_path):
                    for file_name in os.listdir(handlers_path):
                        if file_name.endswith(".py") and file_name != "__init__.py":
                            module_name = f"client.handlers.{file_name[:-3]}" # Исправлен импорт
                            try:
                                module = importlib.import_module(module_name)
                                if hasattr(module, "register"):
                                    module.register(client) # Передаем client
                                else:
                                    logging.warning(f"Модуль {module_name} не содержит функции register.")
                            except ImportError as e:
                                logging.error(f"Ошибка при импорте модуля {module_name}: {e}")
                            except Exception as e:
                                logging.exception(f"Неожиданная ошибка при регистрации обработчиков из {module_name}:")
                create_cache_table()
                await on_startup(client)
                self.bot_task = asyncio.create_task(client.run_until_disconnected())
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.show_message("Успех", "Клиент запущен", QMessageBox.Information)

            except Exception as e:
                logging.exception("Client start error:")
                self.show_message("Ошибка", f"Ошибка запуска клиента: {e}", QMessageBox.Critical)

    def start_client(self):
        if self.bot_task is None:
            self.bot_task = asyncio.ensure_future(self.start_client_async())

    def stop_client(self):
        if self.bot_task:
            try:
                self.bot_task.cancel()
                async def shutdown_client():
                    await on_shutdown(client)
                asyncio.run(shutdown_client())
                self.bot_task = None
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.show_message("Успех", "Клиент остановлен", QMessageBox.Information)
            except asyncio.CancelledError:
                logging.info("Client shutdown cancelled.")
            except Exception as e:
                logging.exception("Ошибка при остановке клиента:")
                self.show_message("Ошибка", f"Ошибка при остановке клиента: {e}", QMessageBox.Critical)
        else:
            self.show_message("Предупреждение", "Клиент не запущен.", QMessageBox.Warning)

    def clear_cache(self):
        try:
            cleanup_cache()
            logging.info("Cache cleared manually.")
            self.show_message("Success", "Cache cleared.", QMessageBox.Information)
        except Exception as e:
            logging.error(f"Error clearing cache: {e}")
            self.show_message("Error", f"Error clearing cache: {e}", QMessageBox.Critical)
# ... (Предыдущий код: __init__, add_log_message, show_message, message_selected, send_reply, start_client_async, start_client, stop_client, clear_cache)
        self.log_widget = self.findChild(QPlainTextEdit, "log_widget")
        self.log_widget.setReadOnly(True)
        self.message_input = self.findChild(QPlainTextEdit, "message_input")
        self.chat_id_input = self.findChild(QLineEdit, "chat_id_input")
        self.clear_cache_button.clicked.connect(self.clear_cache)
        self.send_message_button.clicked.connect(self.send_message)
        self.messages_list = self.findChild(QListWidget, "messages_list")
        self.reply_input = self.findChild(QPlainTextEdit, "reply_input")
        self.send_reply_button = self.findChild(QPushButton, "send_reply_button")
        self.clear_chat_button = self.findChild(QPushButton, "clear_chat_button")
        self.connection_status_label = self.findChild(QLabel, "connection_status_label") # Индикатор состояния
        self.start_button = self.findChild(QPushButton, "start_button")
        self.stop_button = self.findChild(QPushButton, "stop_button")

        self.send_reply_button.clicked.connect(self.send_reply)
        self.clear_chat_button.clicked.connect(self.clear_chat)
        self.start_button.clicked.connect(self.start_client)
        self.stop_button.clicked.connect(self.stop_client)

        self.selected_message_id = None
        self.messages_list.itemClicked.connect(self.message_selected)
        self.bot_task = None
        self.message_items = {}
        self.connection_timer = QTimer(self)
        self.connection_timer.timeout.connect(self.check_connection)
        self.connection_timer.start(5000)  # Проверка каждые 5 секунд

    def check_connection(self):
         if client.is_connected():
             self.connection_status_label.setText("Connected")
             self.connection_status_label.setStyleSheet("color: green;")
         else:
             self.connection_status_label.setText("Disconnected")
             self.connection_status_label.setStyleSheet("color: red;")

    async def send_message(self):
        try:
            chat_id = int(self.chat_id_input.text())
            message_text = self.message_input.toPlainText()
            if message_text:
                await client.send_message(chat_id, message_text)
                self.message_input.clear()
        except ValueError:
            self.show_message("Ошибка", "Некорректный ID чата.", QMessageBox.Critical)
        except Exception as e:
            self.show_message("Error", str(e), QMessageBox.Critical)

# async def main():
    # Запуск polling
    # await dp.start_polling()

async def on_startup(client):
    logging.info("Клиент запущен")
    try:
        await client(UpdateStatusRequest(offline=False)) # Устанавливаем статус "в сети"
    except Exception as e:
        logging.error(f"Error setting online status: {e}")
    asyncio.create_task(periodic_cache_cleanup())

async def on_shutdown(client):
    logging.warning("Клиент выключается...")
    try:
        await client(UpdateStatusRequest(offline=True))  # Устанавливаем статус "не в сети" перед отключением
    except Exception as e:
        logging.error(f"Error setting offline status: {e}")
    await client.disconnect()

async def periodic_cache_cleanup():
    while True:
        cleanup_cache()
        await asyncio.sleep(86400)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    from PyQt5.QtCore import Qt
    window = MainWindow()
    window.show()
    # asyncio.run(main())
    sys.exit(app.exec_())