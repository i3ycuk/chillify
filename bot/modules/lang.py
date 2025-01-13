from brain import asyncio, InlineKeyboardMarkup, InlineKeyboardButton, LANGUAGES_TRANSLATIONS, LANGUAGES_PER_PAGE, LANGUAGES_FLAGS, localization, dp, bot, types, get_user_language, message_cache, logging, connect_db

# Генерация клавиатуры выбора языка
def generate_language_keyboard(page=0):
    keyboard = InlineKeyboardMarkup(row_width=2)
    translations = LANGUAGES_TRANSLATIONS.get(localization.lang, LANGUAGES_TRANSLATIONS["en"])
    start_index = page * LANGUAGES_PER_PAGE
    end_index = start_index + LANGUAGES_PER_PAGE

    language_codes = list(translations.keys())
    for code in language_codes[start_index:end_index]:
        name = translations[code]
        flag = LANGUAGES_FLAGS.get(code, "️")
        keyboard.add(InlineKeyboardButton(f"{flag} {name}", callback_data=f"set_lang_{code}"))

    if page > 0:
        back_text = localization.get("to_back")
        keyboard.add(InlineKeyboardButton(back_text, callback_data=f"lang_page_{page - 1}"))

    if end_index < len(language_codes):
        go_text = localization.get("to_go")
        keyboard.add(InlineKeyboardButton(go_text, callback_data=f"lang_page_{page + 1}"))

    return keyboard


# Отправка выбора языка
async def send_language_picker(message: types.Message):
    user_id = message.from_user.id
    language = get_user_language(user_id) or "en"
    localization.set_language(language)
    keyboard = generate_language_keyboard()

    if message.chat.type != 'private':
        try:
            group_bot_message = await message.reply(localization.get("go_to_private_message"))
            message_cache[user_id] = {"group_message_id": message.message_id, "group_bot_message_id": group_bot_message.message_id}
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения в группу: {e}")
            return
        
        # Попробуем отправить меню в личные сообщения
        try:
            private_bot_message = await bot.send_message(user_id, localization.get("choose_language"), reply_markup=keyboard)
            message_cache[user_id]["private_message_id"] = private_bot_message.message_id
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения в личку пользователю {user_id}: {e}")
            return
    else:
        try:
            await bot.send_message(user_id, localization.get("choose_language"), reply_markup=keyboard)
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения в личку пользователю {user_id}: {e}")

async def safe_delete_message(chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id, message_id)
        logging.debug(f"Сообщение {message_id} в чате {chat_id} успешно удалено.")
    except Exception as e:
        if "сообщение не найдено" in str(e).lower():
            logging.debug(f"Сообщение {message_id} уже удалено или недоступно в чате {chat_id}.")
        else:
            logging.error(f"Ошибка удаления сообщения {message_id} в чате {chat_id}: {e}")


# Обработка выбора языка
@dp.callback_query_handler(lambda c: c.data.startswith('set_lang_'))
async def language_callback(callback_query: types.CallbackQuery):
    language_code = callback_query.data.split('_')[2]
    user_id = callback_query.from_user.id
    localization.set_language(get_user_language(user_id) or "en")

    # Сохранение языка в базу данных
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET language = %s WHERE id = %s", (language_code, user_id))
                conn.commit()
        logging.debug(f"Пользователь {user_id} установил язык: {language_code}.")
    except Exception as e:
        logging.error(f"Ошибка установки языка для пользователя {user_id}: {e}")
        await callback_query.answer(localization.get("lang_update_error"), show_alert=True)
        return

    # Уведомление пользователя и удаление сообщений
    await callback_query.answer(f"{LANGUAGES_TRANSLATIONS.get(language_code, {}).get(language_code, language_code)} {localization.get('lang_selected')}")
    try:
        await safe_delete_message(callback_query.message.chat.id, callback_query.message.message_id)

        message_data = message_cache.get(user_id, {})
        if not message_data:
                logging.debug(f"Кэш сообщений для пользователя {user_id} пуст.")
                return
        if message_data:
            if message_data.get("group_message_id"):
                await safe_delete_message(callback_query.message.chat.id, message_data["group_message_id"])
            if message_data.get("group_bot_message_id"):
                await safe_delete_message(callback_query.message.chat.id, message_data["group_bot_message_id"])
            if message_data.get("private_message_id"):
                await safe_delete_message(user_id, message_data["private_message_id"])

            # message_cache.pop(user_id, None)  # Очищаем кэш после успешного удаления
    except Exception as e:
        logging.error(f"Ошибка очистки кэша сообщений: {e}")


# Обработка смены страницы выбора языка
@dp.callback_query_handler(lambda c: c.data.startswith('lang_page_'))
async def language_page_callback(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split('_')[2])
    user_id = callback_query.from_user.id
    language = get_user_language(user_id) or "en"
    localization.set_language(language)
    keyboard = generate_language_keyboard(page=page)

    try:
        await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=keyboard)
        await callback_query.answer()
    except Exception as e:
        logging.error(f"Ошибка редактирования сообщения в ответ: {e}")


# Регистрация хендлеров
def register(dp):
    dp.register_message_handler(send_language_picker, commands=["lang"])
    logging.debug("Модуль lang: успешно настроен.")
