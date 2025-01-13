from brain import types, text, bold, italic, code, pre, log_stream, dominate, style, body, h1, p, datetime, footer, InlineKeyboardMarkup, InlineKeyboardButton, os, logging, subprocess, sys, Dispatcher, random, choice, SendReactionRequest, ReactionEmoji, AVAILABLE_REACTIONS, client, dp

async def debug_handler(message: types.Message):
    if not message.text:  # Если текста нет
        logging.debug("Пустое сообщение.")
        return

    print(f"Получено сообщение: {message.text}")
    debug_info = text(
        "🛠️ " + bold("Отладочная информация:"),
        f"📄 ID сообщения: {message.message_id}",
        f"💬 Текст: {italic(message.text or 'Нет текста')}",
        f"🕒 Дата и время: {message.date}",
        f"👤 Отправитель: {bold(message.from_user.full_name)}",
        f"🆔 ID отправителя: {message.from_user.id}",
        f"🌐 Язык: {message.from_user.language_code}",
        f"💬 Тип чата: {italic(message.chat.type)}",
        f"🆔 ID чата: {message.chat.id}",
        "📜 " + code("Полный объект сообщения:"),
        pre(str(message.to_python())),  # Преобразуем объект в словарь
        sep="\n",
    )

    await message.reply(debug_info, parse_mode="HTML")


async def ping_handler(message: types.Message):
    selected_reaction = random.choice(AVAILABLE_REACTIONS)
    big_reaction = choice([True])  # Случайным образом выбираем big реакцию: random.choice([True, False])
    try:
        # Добавляем реакцию на сообщение
        await client(SendReactionRequest(
            peer=message.chat.id,
            msg_id=message.message_id,
            reaction=[ReactionEmoji(selected_reaction)],
            big=big_reaction
        ))
        logging.debug(f"Получено сообщение: {message.text}")
        await message.reply("🏓 Понг!")
    except Exception as e:
        logging.error(f"Ошибка при добавлении реакции {selected_reaction}: {e}")


async def test_handler(message: types.Message):
    if not message.text:  # Проверяем текст
        return
    logging.debug(f"Получена команда: {message.text}")
    await message.reply("✅ Бот работает!")

async def generate_html_logs(filter_level: str = None) -> str:
    # Перематываем log_stream в начало, чтобы читать содержимое
    log_stream.seek(0)
    logs = log_stream.getvalue()

    # Проверяем наличие логов, если их нет - добавляем сообщение об этом
    if not logs.strip():
        logs = "Логи отсутствуют или пока не записаны."

    # Применение фильтра уровня логов
    if filter_level:
        filtered_logs = "\n".join(
            line for line in logs.splitlines() if f"{filter_level.upper()} -" in line
        )
        if not filtered_logs.strip():  # Если после фильтрации ничего не осталось
            filtered_logs = f"Логи уровня {filter_level.upper()} отсутствуют."
    else:
        filtered_logs = logs

    # Создаем папку logs, если она не существует
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)

    # Создание HTML-документа с помощью dominate
    doc = dominate.document(title="Логи бота")

    with doc.head:
        style(""" 
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
            }
            h1 {
                color: #4CAF50;
            }
            pre {
                background: #f4f4f4;
                border: 1px solid #ddd;
                padding: 10px;
                overflow-x: auto;
            }
            footer {
                margin-top: 20px;
                font-size: 0.9em;
                color: #555;
            }
        """)

    with doc:
        with body():
            h1("📄 Логи бота")
            p(f"Дата генерации: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            pre(filtered_logs)  # Вставляем фильтрованные логи
            footer("Сгенерировано автоматически ботом.")

    # Сохранение HTML-документа
    file_path = os.path.join(log_folder, "logs.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(doc.render())

    return file_path

# Инлайн-клавиатура для выбора уровня логов
def get_logs_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("⚙️ Все логи", callback_data="logs_all"),
        InlineKeyboardButton("ℹ️ INFO", callback_data="logs_info"),
        InlineKeyboardButton("⚠️ WARNING", callback_data="logs_warning"),
        InlineKeyboardButton("❌ ERROR", callback_data="logs_error"),
    )
    keyboard.add(InlineKeyboardButton("🗑️ Удалить сообщение", callback_data="delete_logs"))
    return keyboard

# Обработчик команды для отправки логов
async def console_handler(message: types.Message):
    await message.reply(
        "📊 Выберите уровень логов для генерации PDF:",
        reply_markup=get_logs_keyboard()
    )

# Обработчик инлайн-кнопок
async def callback_handler(callback_query: types.CallbackQuery):
    action = callback_query.data

    # Инициализируем bot_data для хранения списка сообщений с логами
    if not hasattr(callback_query.bot, "bot_data"):
        callback_query.bot.bot_data = {}
    if "log_message_ids" not in callback_query.bot.bot_data:
        callback_query.bot.bot_data["log_message_ids"] = []

    if action.startswith("logs_"):
        filter_level = action.split("_")[1] if action != "logs_all" else None
        file_path = await generate_html_logs(filter_level)

        sent_message = await callback_query.message.answer_document(
            open(file_path, "rb"),
            caption=f"📁 Логи уровня: {filter_level.upper() if filter_level else 'Все'}",
        )
        os.remove(file_path)  # Удаляем файл после отправки

        # Добавляем ID сообщения с логами в список
        callback_query.bot.bot_data["log_message_ids"].append(sent_message.message_id)
        await callback_query.answer("Файл отправлен!")

    elif action == "delete_logs":
        log_message_ids = callback_query.bot.bot_data.get("log_message_ids", [])
        if log_message_ids:
            for log_message_id in log_message_ids:
                try:
                    await callback_query.bot.delete_message(callback_query.message.chat.id, log_message_id)
                except Exception as e:
                    logging.error(f"Не удалось удалить сообщение с логами: {e}")
            # Очищаем список после удаления
            callback_query.bot.bot_data["log_message_ids"].clear()
        await callback_query.message.delete()
        await callback_query.answer("Все сообщения с логами удалены!")

async def restart_handler(message: types.Message):
        await message.reply("⚙️ Получена команда перезапуска.")
        await message.reply("♻️ Бот перезапускается...")
        logging.debug(f"⚙️ Получена команда перезапуска от {message.from_user.username}.")
        logging.info(f"♻️ Бот перезапускается...")
        subprocess.call([sys.executable] + sys.argv)  # Перезапуск текущего скрипта

# Создаем инлайн-клавиатуру с реакциями
def get_reactions_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=6)
    buttons = [InlineKeyboardButton(reaction, callback_data=reaction) for reaction in AVAILABLE_REACTIONS]
    keyboard.add(*buttons)
    return keyboard

async def reactlist(message: types.Message):
    await message.reply("Выберите реакцию:", reply_markup=get_reactions_keyboard())

async def process_callback_reaction(callback_query: types.CallbackQuery):
    selected_reaction = callback_query.data
    message_id = callback_query.message.reply_to_message.message_id  # ID сообщения, на которое ответил бот
    chat_id = callback_query.message.chat.id
    big_reaction = choice([True])

    try:
        # Добавляем реакцию на сообщение
        await client(SendReactionRequest(
            peer=chat_id,
            msg_id=message_id,
            reaction=[ReactionEmoji(emoticon=selected_reaction)],
            big=big_reaction
        ))
        await callback_query.answer(f'Реакция {selected_reaction} добавлена.')
    except Exception as e:
        logging.error(f"Ошибка при добавлении реакции {selected_reaction}: {e}")
        await callback_query.answer(f'Ошибка при добавлении реакции {selected_reaction}.')

# Регистрация обработчиков
def register(dp: Dispatcher):
    dp.register_message_handler(restart_handler, lambda message: message.text.strip().lower() in ["/restart", "/reboot", "/reset", "restart", "reboot", "reset", "перезагрузить", "перезапустить", "перезапуск", "ребут"])
    dp.register_message_handler(console_handler, lambda message: message.text.strip().lower() in ["/console","/консоль", "console", "консоль", "/logs","/логи", "logs", "логи"])
    dp.register_callback_query_handler(callback_handler, lambda c: c.data.startswith("logs_") or c.data == "delete_logs")
    dp.register_message_handler(test_handler, commands=["test", "тест", "check", "проверка", "чек"])
    dp.register_message_handler(debug_handler, lambda message: message.text and message.text.strip().lower() in ["debug", "дебаг", "инфа", "отладка", "test", "тест", "check", "проверка", "чек"])
    dp.register_message_handler(ping_handler, lambda message: message.text and message.text.strip().lower() in ["пинг", "ping"])
    dp.register_message_handler(reactlist, lambda message: message.text and message.text.strip().lower() in ["react", "реакт"])
    dp.register_callback_query_handler(process_callback_reaction, lambda c: c.data in AVAILABLE_REACTIONS)
    logging.debug("Модуль test: успешно настроен.")
