from brain import logging, dp, BotBlocked, StringIO, connect_db, psycopg2, asyncio, bot, os

# Создаем папку logs, если она не существует
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)

# Путь к файлу логов
log_file_path = os.path.join(log_folder, "bot.log")

# Настраиваем логирование
log_stream = StringIO()
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логов (DEBU в production)
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    encoding="utf-8",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),  # Запись в файл
        logging.StreamHandler(),  # Вывод в консоль
        logging.StreamHandler(log_stream)  # Запись в StringIO
    ]
)

# Ошибка: BotBlocked
@dp.errors_handler()
async def error_handler(update, exception):
    logging.exception("Произошла ошибка:") # Логируем полный трейсбек
    if isinstance(exception, BotBlocked):
        user_id = update.effective_user.id # Получаем ID пользователя
        logging.warning(f"Бот заблокирован пользователем {user_id}. Удаление пользователя из базы данных.")
        try:
            with connect_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    conn.commit()
            logging.info(f"Пользователь {user_id} успешно удален из базы данных.")
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Ошибка при удалении пользователя {user_id} из базы данных: {e}")
    return True

logger = logging.getLogger(__name__) # Получаем логгер для текущего модуля
logger.debug("Логи успешно настроены.") # Пример использования debug-уровня

# Новый кэш с автоматической очисткой
message_cache = {}

# Очистка кэша каждые сутки
async def clear_cache_daily():
    while True:
        await asyncio.sleep(86400)  # 24 часа
        message_cache.clear()
        logging.debug("Кэш сообщений успешно очищен.")
