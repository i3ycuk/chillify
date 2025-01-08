from brain import logging, dp, BotBlocked, StringIO, connect_db, psycopg2, asyncio, bot

# Настраиваем логирование
log_stream = StringIO()
logging.basicConfig(
    level=logging.INFO, # Уровень логов (INFO в production)
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", # Добавлено имя логгера
    encoding="utf-8",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"), # Запись в файл
        logging.StreamHandler() # Вывод в консоль
    ]
)

# Пример записи в логи
logging.info("Бот запущен!")

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
logger.debug("Debug сообщение из logs.py") # Пример использования debug-уровня

# Новый кэш с автоматической очисткой
message_cache = {}

# Очистка кэша каждые сутки
async def clear_cache_daily():
    while True:
        await asyncio.sleep(86400)  # 24 часа
        message_cache.clear()
        logging.info("Message cache has been cleared.")

async def safe_delete_message(chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception as e:
        if "message to delete not found" not in str(e).lower():
            logging.error(f"Error deleting message {message_id} in chat {chat_id}: {e}")
