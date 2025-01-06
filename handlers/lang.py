from brain import InlineKeyboardMarkup, LANGUAGES_TRANSLATIONS, LANGUAGES_PER_PAGE, LANGUAGES_FLAGS, InlineKeyboardButton, localization, dp, types, get_user_language, bot, BotBlocked, message_cache, sqlite3, logging, Dispatcher, connect_db, psycopg2

def generate_language_keyboard(page=0): # Убрали current_language
    keyboard = InlineKeyboardMarkup(row_width=2)
    translations = LANGUAGES_TRANSLATIONS.get(localization.lang, LANGUAGES_TRANSLATIONS["en"]) # Используем localization.lang
    start_index = page * LANGUAGES_PER_PAGE
    end_index = start_index + LANGUAGES_PER_PAGE

    # Получаем переводы языков и добавляем кнопки
    language_codes = list(translations.keys())
    for code in language_codes[start_index:end_index]:
        name = translations[code]
        flag = LANGUAGES_FLAGS.get(code, "🏳️")  # По умолчанию белый флаг
        keyboard.add(InlineKeyboardButton(f"{flag} {name}", callback_data=f"set_lang_{code}"))

    # Навигация по страницам
    if page > 0:
        back_text = localization.get("to_back") # Без current_language
        keyboard.add(InlineKeyboardButton(back_text, callback_data=f"lang_page_{page - 1}"))

    if end_index < len(language_codes):
        go_text = localization.get("to_go") # Без current_language
        keyboard.add(InlineKeyboardButton(go_text, callback_data=f"lang_page_{page + 1}"))

    return keyboard

async def send_language_picker(message: types.Message):
    print(f"Получена команда: {message.text}")
    user_id = message.from_user.id
    chat_id = message.chat.id
    language = get_user_language(user_id) or "en"
    localization.set_language(language)
    keyboard = generate_language_keyboard()

    # Создаем словарь для хранения данных о сообщениях
    bot_message_ids = {}

    # Проверяем, если пользователь не в личных сообщениях, отправляем уведомление в чат
    if message.chat.type != 'private':
        # Отправляем сообщение с просьбой перейти в личные сообщения
        group_bot_message = await message.reply(
            localization.get("go_to_private_message")
        )

        # Сохраняем ID сообщения пользователя и бота в группе
        bot_message_ids["group_user_message_id"] = message.message_id
        bot_message_ids["group_bot_message_id"] = group_bot_message.message_id

    # Отправляем сообщение в ЛС
    try:
        private_bot_message = await bot.send_message(
            user_id,
            localization.get("choose_language"),
            reply_markup=keyboard
        )

        # Если сообщение в группе, сохраняем ID сообщения в личке
        if message.chat.type != 'private':
            bot_message_ids["private_bot_message_id"] = private_bot_message.message_id
    except BotBlocked:
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
    if message.chat.type != 'private':
        await message.reply(localization.get("bot_blocked"))

    # Сохраняем данные о сообщениях в кэш
    message_cache.pop(user_id, None)

@dp.callback_query_handler(lambda c: c.data.startswith('set_lang_'))
async def language_callback(callback_query: types.CallbackQuery):
    # Извлекаем код языка из callback_data
    language_code = callback_query.data.split('_')[2]
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    user_language = get_user_language(user_id)
    localization.set_language(user_language)

    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET language = %s WHERE id = %s", (language_code, user_id))
                conn.commit()
        logging.info(f"Язык пользователя {user_id} успешно обновлен на {language_code}.") # Логирование успешного обновления
    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"Ошибка обновления языка пользователя {user_id}: {e}")
        await callback_query.answer("Произошла ошибка при обновлении языка.", show_alert=True)
        return

    # Отправляем сообщение с подтверждением
    await bot.answer_callback_query(
        callback_query.id,
        text=f"{LANGUAGES_TRANSLATIONS[language_code][language_code]} {localization.get('lang_selected')}"
    )

    # Удаляем сообщение с клавиатурой в ЛС
    try:
        await bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id
        )
    except Exception as e:
        logging.error(f"Ошибка при удалении сообщения с клавиатурой: {e}")

    # Получаем данные о сообщениях из кэша
    bot_message_ids = message_cache.get(user_id, {}).get(chat_id, {}) # Исправлено

    # Если сообщения в кэше нет, пропускаем удаление
    if not bot_message_ids:
        logging.warning(f"Нет данных о сообщениях для пользователя {id} в чате {chat_id}")
        return

    # Удаляем сообщения в группе
    group_user_message_id = bot_message_ids.get("group_user_message_id")
    group_bot_message_id = bot_message_ids.get("group_bot_message_id")

    if group_user_message_id:
        try:
            await bot.delete_message(
                chat_id=callback_query.message.chat.id,
                message_id=group_user_message_id
            )
        except Exception as e:
            logging.error(f"Ошибка при удалении сообщения пользователя в группе: {e}")

    if private_bot_message_id:
        try:
            await bot.delete_message(
                chat_id=user_id, # Исправлено
                message_id=private_bot_message_id
            )
        except Exception as e:
            logging.error(f"Ошибка при удалении сообщения бота в группе: {e}")

    # Удаляем сообщение с командой /lang в личке
    private_bot_message_id = bot_message_ids.get("private_bot_message_id")
    if private_bot_message_id:
        try:
            await bot.delete_message(
                chat_id=id,
                message_id=private_bot_message_id
            )
        except Exception as e:
            logging.error(f"Ошибка при удалении сообщения с командой /lang в ЛС: {e}")

    # Очищаем кэш после удаления сообщений
    message_cache.pop(user_id, None)

@dp.callback_query_handler(lambda c: c.data.startswith('lang_page_'))
async def language_page_callback(callback_query: types.CallbackQuery):
    # Извлекаем номер страницы
    page = int(callback_query.data.split('_')[2])
    user_id = callback_query.from_user.id
    language = get_user_language(user_id) or "en"
    localization.set_language(language) # Устанавливаем язык для localization!
    keyboard = generate_language_keyboard(page=page) # Без current_language

    # Отправляем обновленную клавиатуру
    await bot.edit_message_reply_markup(
        callback_query.message.chat.id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )
    # Отвечаем на callback_query
    await bot.answer_callback_query(callback_query.id)
    
def register(dp: Dispatcher):
    dp.register_message_handler(send_language_picker, commands=["lang"])
    print("lang успешно зарегистрирован.")