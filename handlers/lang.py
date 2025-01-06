from brain import localization, InlineKeyboardMarkup, InlineKeyboardButton, get_user, add_user, logger, psycopg2, bot, MessageToDeleteNotFound, MessageCantBeDeleted, exceptions, update_user_messages, types, Dispatcher

def start_keyboard(language):
    localization.set_language(language)
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(localization.get("button_quotes"), callback_data="quotes"),
        InlineKeyboardButton(localization.get("button_memes"), callback_data="memes"),
        InlineKeyboardButton(localization.get("button_relax"), callback_data="relax"),
        InlineKeyboardButton(localization.get("button_settings"), callback_data="settings"),
    ]
    keyboard.add(*buttons)
    return keyboard

async def greet_user(message: types.Message, data: dict):
    user_id = message.from_user.id
    user_data = get_user(user_id)

    if not user_data:  # Новый пользователь
        if message.from_user and message.from_user.language_code:
            language = message.from_user.language_code
            try:
                add_user(user_id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, None, None, language)
                logger.info(f"New user {user_id} added with language from API: {language}")
            except psycopg2.Error as e:
                logger.error(f"Error adding new user {user_id} with language from API: {e}")
                language = "en"
                add_user(user_id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, None, None, language, status="waiting_for_language")
                logger.info(f"New user {user_id} added with default language due to error: {language}")
        else:
            language = "en"  # Язык по умолчанию
            try:
                add_user(user_id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, None, None, language, status="waiting_for_language")
                logger.info(f"New user {user_id} added with default language: {language}")
            except psycopg2.Error as e:
                logger.error(f"Error adding new user {user_id} with default language: {e}")
                return

        localization.set_language(language)
        await message.reply(localization.get("choose_language_message"))
        return

    else:  # Пользователь уже есть в БД
        language = user_data["language"]
        localization.set_language(language)

        if user_data.get("last_start_message_id") and user_data.get("last_bot_message_id"):
            try:
                await bot.delete_message(message.chat.id, user_data["last_start_message_id"])
                await bot.delete_message(message.chat.id, user_data["last_bot_message_id"])
                logger.info(f"Old messages for user {user_id} deleted.")
            except MessageToDeleteNotFound:
                logger.warning(f"Сообщение для пользователя {user_id} уже удалено.")
            except MessageCantBeDeleted:
                logger.warning(f"Не удалось удалить сообщение для пользователя {user_id}. Возможно, у бота недостаточно прав.")
            except exceptions.TelegramForbidden as e:
                logger.warning(f"Bot is blocked by user: {e}")
                return

        if message.chat.type == 'private':
            greeting_message = localization.get("private_welcome")
        else:
            greeting_message = localization.get("group_welcome")

        bot_message = await message.reply(greeting_message, reply_markup=start_keyboard(language))
        try:
            update_user_messages(user_id, message.message_id, bot_message.message_id)
            logger.info(f"Message IDs for user {user_id} updated in database.")
        except psycopg2.Error as e:
            logger.error(f"Error updating message IDs for user {user_id}: {e}")

async def send_start_menu(message: types.Message, data: dict):
    user_id = message.from_user.id
    user_data = get_user(user_id)

    if user_data:
        language = user_data["language"]
        localization.set_language(language)
        if user_data.get("last_start_message_id") and user_data.get("last_bot_message_id"):
            try:
                await bot.delete_message(message.chat.id, user_data["last_start_message_id"])
                await bot.delete_message(message.chat.id, user_data["last_bot_message_id"])
                logger.info(f"Old messages for user {user_id} deleted.")
            except MessageToDeleteNotFound:
                logger.warning(f"Сообщение для пользователя {user_id} уже удалено.")
            except MessageCantBeDeleted:
                logger.warning(f"Не удалось удалить сообщение для пользователя {user_id}. Возможно, у бота недостаточно прав.")
            except exceptions.TelegramForbidden as e:
                logger.warning(f"Bot is blocked by user: {e}")
                return

        bot_message = await message.reply(localization.get("start_message"), reply_markup=start_keyboard(language))
        try:
            update_user_messages(user_id, message.message_id, bot_message.message_id)
            logger.info(f"Message IDs for user {user_id} updated in database.")
        except psycopg2.Error as e:
            logger.error(f"Error updating message IDs for user {user_id}: {e}")

def register_start(dp: Dispatcher):
    dp.register_message_handler(greet_user, commands=["start"])
    dp.register_message_handler(send_start_menu, commands=["menu"])
    logger.info("start registered.")