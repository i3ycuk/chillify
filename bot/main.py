from pathlib import Path
import sys

# Добавляем корень проекта в sys.path
project_root = Path(__file__).resolve().parent.parent  # Переход на два уровня вверх
sys.path.append(str(project_root))

# Теперь можно импортировать brain.py
from brain import Dispatcher, os, importlib, logging, dp, create_db, executor, localization, asyncio, clear_cache_daily

def register_handlers_from_directory(dp, handlers_dir="modules"):
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
                    logging.debug(f"Модуль {file_name}: не имеет регистрации.")
            except ImportError as e:
                logging.error(f"Ошибка при импорте модуля {file_name}: {e}")
            except Exception as e:
                logging.exception(f"Неожиданная ошибка при регистрации обработчиков из {file_name}:") # Логируем полный traceback

# Регистрируем обработчики
logging.debug("Регистрация модулей...")
register_handlers_from_directory(dp)
logging.debug("Регистрация модулей: завершена.")



async def main():
    # Запуск polling
    logging.debug("Запуск бота...")
    await dp.start_polling()
    logging.debug("Бот успешно запустился.")

async def on_startup(dispatcher):
    asyncio.create_task(clear_cache_daily())
    logging.debug("Служба очистки кэша был успешно запущен.")

# Запуск бота
if __name__ == '__main__':
    create_db()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)