from brain import Dispatcher, os, importlib, logging, dp, create_db, executor, localization, BaseMiddleware, types, get_user_language

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

# Middleware для локализации
class LocalizationMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        language = get_user_language(user_id) or "en"
        data["language"] = language

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        user_id = callback_query.from_user.id
        language = get_user_language(user_id) or "en"
        data["language"] = language

# Регистрация middleware
dp.middleware.setup(LocalizationMiddleware())
async def main():
    # Запуск polling
    await dp.start_polling()

# Запуск бота
if __name__ == '__main__':
    create_db()
    executor.start_polling(dp, skip_updates=True)