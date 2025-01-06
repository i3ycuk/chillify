from brain import dp, psycopg2, types, localization, get_user_language, logger, InlineKeyboardMarkup, InlineKeyboardButton, bot, add_user, get_random_quote, get_random_meme, get_relax_message, get_gif, Dispatcher

async def greet_user(message: types.Message, data: dict):
    language = data.get("language")
    localization.set_language(language)

    if message.chat.type == 'private':
        greeting_message = localization.get("private_welcome")
    else:
        greeting_message = localization.get("group_welcome")
    await message.reply(greeting_message)

async def send_start_menu(message: types.Message, data: dict):
    language = data.get("language")
    localization.set_language(language)

    user_id = message.from_user.id
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
        add_user(user_id, first_name, last_name, username, None, None, language) # Используем язык из data
        logger.info(f"User {user_id} added to the database.")
    except psycopg2.Error as e:
        logger.error(f"Error adding user {user_id} to the database: {e}")
        await message.reply(localization.get("registration_error"))
        return

    await message.reply(localization.get("start_message"), reply_markup=keyboard)

async def handle_quotes(callback_query: types.CallbackQuery, data: dict):
    language = data.get("language")
    localization.set_language(language)
    quote = get_random_quote()
    await bot.send_message(callback_query.message.chat.id, quote)

async def handle_memes(callback_query: types.CallbackQuery, data: dict):
    language = data.get("language")
    localization.set_language(language)
    meme = get_random_meme()
    await bot.send_message(callback_query.message.chat.id, meme)

async def handle_relax(callback_query: types.CallbackQuery, data: dict):
    language = data.get("language")
    localization.set_language(language)
    relax_msg = get_relax_message()
    gif_url = get_gif("relax")
    if gif_url:
        await bot.send_animation(callback_query.message.chat.id, gif_url, caption=relax_msg)
    else:
        await bot.send_message(callback_query.message.chat.id, relax_msg)

async def handle_callback(callback_query: types.CallbackQuery, data: dict):
    language = data.get("language")
    localization.set_language(language)
    callback_data = callback_query.data
    handlers = {
        "quotes": handle_quotes,
        "memes": handle_memes,
        "relax": handle_relax,
    }
    handler = handlers.get(callback_data)
    if handler:
        await handler(callback_query, data) # Передаем data в обработчики
    else:
        logger.warning(f"Unknown callback data: {callback_data}")

    await bot.answer_callback_query(callback_query.id)

def register(dp: Dispatcher):
    dp.register_message_handler(greet_user, commands=["start"])  # Убрали pass_args=True
    dp.register_message_handler(send_start_menu, commands=["menu"])  # Убрали pass_args=True
    dp.register_callback_query_handler(handle_callback, lambda c: c.data and c.data in ['quotes', 'memes', 'relax']) # Убрали pass_args=True
    logger.info("start registered.")