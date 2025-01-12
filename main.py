from brain import Dispatcher, os, importlib, logging, dp, bot, create_db, executor, localization, asyncio, clear_cache_daily, sys, QApplication, sqlite3, threading, time, datetime, timedelta, QMessageBox, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QPlainTextEdit, QMessageBox

def register_handlers_from_directory(dp, handlers_dir="handlers"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    handlers_path = os.path.join(base_dir, handlers_dir)

    if not os.path.exists(handlers_path):
        raise FileNotFoundError(f"Папка '{handlers_dir}' не найдена.")

    init_file = os.path.join(handlers_path, "__init__.py")
    if not os.path.exists(init_file):
        logging.warning(f"В папке '{handlers_dir}' отсутствует файл '__init__.py'. Возможны проблемы с импортом.")

    for file_name in os.listdir(handlers_path):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_name = f"{handlers_dir}.{file_name[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "register"):
                    module.register(dp)
                else:
                    logging.warning(f"Модуль {module_name} не содержит функции register.")
            except ImportError as e:
                logging.error(f"Ошибка при импорте модуля {module_name}: {e}")
            except Exception as e:
                logging.exception(f"Неожиданная ошибка при регистрации обработчиков из {module_name}:") # Логируем полный traceback


async def main():
    # Запуск polling
    await dp.start_polling()

async def on_startup(dispatcher):
    asyncio.create_task(clear_cache_daily())
    logging.info("Бот запущен")

async def on_shutdown(dispatcher: Dispatcher):
    logging.warning("Бот выключается...")
    await bot.close()
    # Здесь можно добавить логику завершения, например, закрытие соединения с БД

bot_instance = None # Экземпляр бота
bot_task = None # Задача для запуска бота

async def start_bot_async(window): # Делаем функцию асинхронной
    global bot_task
    if bot_task is None:
        # Регистрируем обработчики
        print("Запуск регистрации обработчиков.")
        register_handlers_from_directory(dp) # Регистрируем обработчики
        print("Регистрация обработчиков завершена.")
        print("Начинаем polling...")
        try:
            await on_startup(dp) # Вызываем on_startup
            await create_db(), executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
        except Exception as e:
            logging.exception("Bot polling error:")
            window.show_message("Error", f"Bot polling error: {e}", QMessageBox.Critical)
        finally:
            await on_shutdown(dp) # Вызываем on_shutdown при любом исходе
            bot_task = None # Обнуляем задачу после завершения
            window.start_button.setEnabled(True)
            window.stop_button.setEnabled(False)
            logging.info("Bot stopped.")
            window.show_message("Success", "Bot stopped", QMessageBox.Information)
    else:
        window.show_message("Warning", "Bot is already running.", QMessageBox.Warning)

def start_bot(window):
    global bot_task
    if bot_task is None:
        bot_task = asyncio.ensure_future(start_bot_async(window)) # Запускаем асинхронную функцию в asyncio


def stop_bot(window):
    if dp and dp.bot:  # Проверка на None
        async def shutdown_bot():
            await dp.stop_polling()
            await dp.bot.close()
        try:
            asyncio.run(shutdown_bot())
        except Exception as e:
            logging.exception("Error during bot shutdown:")
            window.show_message("Error", f"Error during bot shutdown: {e}", QMessageBox.Critical)

DATABASE_FILE = "message_cache.db"
EXPIRATION_TIME = timedelta(days=1)

def create_cache_table():
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS message_cache (
                    user_id INTEGER PRIMARY KEY,
                    group_message_id INTEGER,
                    group_bot_message_id INTEGER,
                    private_message_id INTEGER,
                    expire_time TEXT
                )
            """)
            conn.commit()
        logging.info("Cache table created (or already exists).")
    except sqlite3.Error as e:
        logging.error(f"Error creating cache table: {e}")

def store_message_data(user_id, group_message_id=None, group_bot_message_id=None, private_message_id=None):
    expire_time = (datetime.utcnow() + EXPIRATION_TIME).isoformat()
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO message_cache (user_id, group_message_id, group_bot_message_id, private_message_id, expire_time)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, group_message_id, group_bot_message_id, private_message_id, expire_time))
            conn.commit()
        logging.info(f"Stored message data for user {user_id}.")
    except sqlite3.Error as e:
        logging.error(f"Error storing message data: {e}")

def get_message_data(user_id):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM message_cache WHERE user_id = ?", (user_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Error getting message data: {e}")
        return None

def delete_message_data(user_id):
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM message_cache WHERE user_id = ?", (user_id,))
            conn.commit()
        logging.info(f"Deleted message data for user {user_id}.")
    except sqlite3.Error as e:
        logging.error(f"Error deleting message data: {e}")

def cleanup_cache():
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            now = datetime.datetime.utcnow().isoformat()  # Только для Python < 3.12
            cursor.execute("DELETE FROM message_cache WHERE expire_time < ?", (now,))
            conn.commit()
        logging.info("Expired cache entries cleaned up.")
    except sqlite3.Error as e:
        logging.error(f"Error cleaning up cache: {e}")

def clear_cache(window):
    try:
        clear_cache()
        logging.info("Cache cleared manually.")
        window.show_message("Success", "Cache cleared.", QMessageBox.Information)

    except Exception as e:
        logging.error(f"Error clearing cache: {e}")
        window.show_message("Error", f"Error clearing cache: {e}", QMessageBox.Critical)

def cleanup_cache_thread():
    create_cache_table()
    while True:
        cleanup_cache()
        time.sleep(86400) # 24 часа

def start_cache_cleanup():
    threading.Thread(target=cleanup_cache_thread, daemon=True).start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chillify Launcher")

        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)

        self.start_button = QPushButton("Start Bot")
        self.stop_button = QPushButton("Stop Bot")
        self.clear_cache_button = QPushButton("Clear Cache")

        layout = QVBoxLayout()
        layout.addWidget(self.log_widget)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.clear_cache_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_log_message(self, message):
        self.log_widget.appendPlainText(message + "\n")
        self.log_widget.verticalScrollBar().setValue(self.log_widget.verticalScrollBar().maximum()) # Автопрокрутка

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()


class QtHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        message = self.format(record)
        self.widget.add_log_message(message)

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()

    # Настройка логирования для вывода в виджет и файл
    qt_handler = QtHandler(window)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    qt_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('launcher.log', mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(qt_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)

    return app, window

# Запуск бота
if __name__ == "__main__":
    app, window = run_gui()
    logging.basicConfig(filename='launcher.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    start_cache_cleanup()

    window.start_button.clicked.connect(lambda: start_bot(window))
    window.stop_button.clicked.connect(lambda: stop_bot(window))
    window.clear_cache_button.clicked.connect(lambda: clear_cache(window))

    window.show()
    sys.exit(app.exec_())
   