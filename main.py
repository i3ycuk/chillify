from brain import Dispatcher, os, importlib, logging, dp, create_db, executor, localization, asyncio, clear_cache_daily, sys, QApplication, run_gui, MainWindow, sqlite3, threading, time, datetime, timedelta, utils, QMessageBox
from brain import dp as brain_dp, bot as brain_bot

bot_instance = None # Экземпляр бота
bot_task = None # Задача для запуска бота

def start_bot(window):
    global bot_instance, bot_task
    if bot_instance is None:
        bot_instance = brain_bot
        brain_register(brain_dp)
        async def run_bot():
            try:
                await brain_dp.start_polling()
            except Exception as e:
                logging.exception("Bot polling error:")
                window.show_message("Error", f"Bot polling error: {e}", QMessageBox.Critical)
        bot_task = asyncio.ensure_future(run_bot())
        window.start_button.setEnabled(False)
        window.stop_button.setEnabled(True)
        logging.info("Bot started.")
        window.show_message("Success", "Bot started", QMessageBox.Information)
    else:
        window.show_message("Warning", "Bot is already running.", QMessageBox.Warning)


def stop_bot(window):
    global bot_instance, bot_task
    if bot_instance:
        async def shutdown_bot():
            await brain_dp.stop_polling()
            await brain_bot.close()
        asyncio.run(shutdown_bot())
        bot_instance = None
        bot_task = None
        window.start_button.setEnabled(True)
        window.stop_button.setEnabled(False)
        logging.info("Bot stopped.")
        window.show_message("Success", "Bot stopped", QMessageBox.Information)
    else:
        window.show_message("Warning", "Bot is not running.", QMessageBox.Warning)

def clear_cache(window):
    try:
        utils.clear_cache()
        logging.info("Cache cleared manually.")
        window.show_message("Success", "Cache cleared.", QMessageBox.Information)

    except Exception as e:
        logging.error(f"Error clearing cache: {e}")
        window.show_message("Error", f"Error clearing cache: {e}", QMessageBox.Critical)

def cleanup_cache_thread():
    utils.create_cache_table()
    while True:
        utils.cleanup_cache()
        time.sleep(86400) # 24 часа

def start_cache_cleanup():
    threading.Thread(target=cleanup_cache_thread, daemon=True).start()

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

# Регистрируем обработчики
print("Запуск регистрации обработчиков.")
register_handlers_from_directory(dp)
print("Регистрация обработчиков завершена.")
print("Начинаем polling...")
print("Бот запущен!")

async def main():
    # Запуск polling
    await dp.start_polling()

async def on_startup(dispatcher):
    asyncio.create_task(clear_cache_daily())
    logging.info("Cache cleaning task has been started.")

# Запуск бота
if __name__ == '__main__':
    app, window = run_gui()
    start_cache_cleanup() # Запуск очистки кэша

    window.start_button.clicked.connect(lambda: start_bot(window)) # Передача окна
    window.stop_button.clicked.connect(lambda: stop_bot(window))
    window.clear_cache_button.clicked.connect(lambda: clear_cache(window))

    window.show()
    sys.exit(app.exec_())

    #create_db()
    #executor.start_polling(dp, skip_updates=True, on_startup=on_startup)