from brain import dp, psycopg2, types, localization, get_user_language, InlineKeyboardMarkup, InlineKeyboardButton, sqlite3, logging, get_random_quote, bot, get_random_meme, get_relax_message, get_gif, Dispatcher, add_user

async def send_welcome(message: types.Message):
    print(f"Получена команда: {message.text}")
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    language = get_user_language(user_id)  # Получаем язык пользователя из базы
    localization.set_language(language)  # Устанавливаем язык для локализации
    birth_date = None  # Здесь можешь добавить логику для получения даты рождения, если нужно
    interests = None  # Здесь можешь добавить логику для получения интересов пользователя, если нужно
    
    # Логика для личных и групповых чатов
    if message.chat.type == 'private':
        await message.reply(localization.get("private_welcome"))
    else:
        await message.reply(localization.get("group_welcome"))

    # Добавляем инлайн кнопки
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_quotes = InlineKeyboardButton(localization.get("button_quotes"), callback_data="quotes")
    button_memes = InlineKeyboardButton(localization.get("button_memes"), callback_data="memes")
    button_relax = InlineKeyboardButton(localization.get("button_relax"), callback_data="relax")
    keyboard.add(button_quotes, button_memes, button_relax)
    await message.reply(localization.get("start_message"), reply_markup=keyboard)

    # Добавляем пользователя в базу данных
    try:
        add_user(user_id, first_name, last_name, username, birth_date, interests, language)
        logging.info(f"Пользователь {user_id} успешно добавлен в базу данных.")
    except psycopg2.Error as e:
        logging.error(f"Ошибка при добавлении пользователя {user_id} в базу данных: {e}")
        await message.reply("Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.") # Сообщение пользователю об ошибке
        return # Прерываем выполнение функции, чтобы избежать дальнейших ошибок

# Обработчик кнопок для инлайн меню
async def handle_callback(callback_query: types.CallbackQuery):
    logging.info(f"Получен callback: {callback_query.data}")  # Логируем вызов
    data = callback_query.data
    chat_id = callback_query.message.chat.id  # ID чата, в котором была нажата кнопка

    if data == 'quotes':
        quote = get_random_quote()
        await bot.send_message(chat_id, quote)  # Отправляем ответ в тот же чат
    elif data == 'memes':
        meme = get_random_meme()
        await bot.send_message(chat_id, meme)  # Отправляем ответ в тот же чат
    elif data == 'relax':
        relax_msg = get_relax_message()
        gif_url = get_gif("relax")
        if gif_url:
            await bot.send_animation(chat_id, gif_url, caption=relax_msg)  # Отправляем анимацию в чат
        else:
            await bot.send_message(chat_id, relax_msg)  # Отправляем текстовое сообщение в чат

    await bot.answer_callback_query(callback_query.id)  # Ответ на инлайн запрос
 
def register(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_callback_query_handler(handle_callback, lambda c: c.data and c.data in ['quotes', 'memes', 'relax'])
    print("start успешно зарегистрирован.")
