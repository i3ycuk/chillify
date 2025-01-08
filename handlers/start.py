from brain import dp, psycopg2, types, localization, get_user_language, logger, InlineKeyboardMarkup, InlineKeyboardButton, bot, add_user, get_random_quote, get_random_meme, get_relax_message, get_gif, Dispatcher, partial, FSMContext, get_user, CommandStart, logging, CallbackData

async def greet_user(message: types.Message, state: FSMContext):  # Use state
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    language_code = message.from_user.language_code

    user_data = get_user(user_id)

    if not user_data:  # New user
        language_code = message.from_user.language_code
        if language_code:
            localization.set_language(language_code)
            add_user(user_id=user_id, first_name=first_name, last_name=last_name, username=username, language=language_code)  # Create user in DB
            if message.chat.type == types.ChatType.PRIVATE:
                await message.answer(localization.get("private_welcome"))
            else:
                await message.answer(localization.get("group_welcome"))
        else:  # language_code not received
            localization.set_language("en")  # Default language
            add_user(user_id, "en", status="waiting_for_language")  # Create user with waiting status
            await message.answer(localization.get("choose_language"))
    else:  # Existing user
        language = user_data["language"]
        localization.set_language(language)
        if message.chat.type == types.ChatType.PRIVATE:
            await message.answer(localization.get("private_welcome"))
        else:
            await message.answer(localization.get("group_welcome"))
    await send_start_menu(message, state)

async def send_start_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user(user_id)
    if not user_data:
        logging.error(f"User with ID {user_id} not found in database when trying to send start menu.")
        return  # Important check to avoid KeyError

    language = user_data["language"]
    localization.set_language(language)

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(localization.get("button_quotes"), callback_data="quotes"),
        InlineKeyboardButton(localization.get("button_memes"), callback_data="memes"),
        InlineKeyboardButton(localization.get("button_relax"), callback_data="relax"),
    ]
    keyboard.add(*buttons)


    try:
        add_user(user_id, first_name, last_name, username, None, None, language)
        logger.info(f"User {user_id} data potentially updated in send_start_menu.") # Более точное сообщение
    except psycopg2.Error as e:
        logger.error(f"Database error (send_start_menu): {e}")
        await message.reply(localization.get("registration_error"))
        return

    await message.reply(localization.get("start_message"), reply_markup=keyboard)

async def handle_menu_callback(callback_query: types.CallbackQuery):  # callback_data больше не передается
    item = callback_query.data  # Получаем callback_data как строку
    user_id = callback_query.from_user.id
    user_data = get_user(user_id)
    if not user_data:
        logging.error(f"User with ID {user_id} not found.")
        return
    language = user_data["language"]
    localization.set_language(language)
    handlers = {
        "quotes": handle_quotes,
        "memes": handle_memes,
        "relax": handle_relax,
    }
    handler = handlers.get(item)
    if handler:
        await handler(callback_query)
    else:
        logger.warning(f"Unknown menu item: {item}")

    await callback_query.answer()


async def handle_quotes(callback_query: types.CallbackQuery):
    quote = get_random_quote()
    await bot.send_message(callback_query.message.chat.id, quote)

async def handle_memes(callback_query: types.CallbackQuery):
    meme = get_random_meme()
    await bot.send_message(callback_query.message.chat.id, meme)

async def handle_relax(callback_query: types.CallbackQuery):
    relax_msg = get_relax_message()
    gif_url = get_gif("relax")
    if gif_url:
        await bot.send_animation(callback_query.message.chat.id, gif_url, caption=relax_msg)
    else:
        await bot.send_message(callback_query.message.chat.id, relax_msg)


def register(dp: Dispatcher):
    dp.register_message_handler(greet_user, CommandStart())
    dp.register_message_handler(send_start_menu, commands=["menu"])
    dp.register_callback_query_handler(handle_menu_callback, lambda c: c.data in ["quotes", "memes", "relax"]) # Фильтрация с помощью lambda
    logger.info("start registered.")