from brain import types, executor, asyncio, logging, dp, random, logger, bot, Dispatcher

# Данные игры
games = {}

# Слова для игры
words = [
    ("Пляж", "Пустыня"),
    ("Кафе", "Ресторан"),
    ("Горы", "Лес"),
    ("Самолёт", "Поезд"),
    ("Театр", "Кинотеатр"),
    ("Космос", "Звезды"),
    ("Пират", "Корабль"),
    ("Школа", "Университет"),
    ("Машина", "Автобус"),
    ("Супермаркет", "Магазин"),
]

# Статистика
game_statistics = {}

# Команда для запуска игры
async def start_game(message: types.Message):
    chat_id = message.chat.id
    if chat_id in games:
        await message.reply("Игра уже запущена! Присоединяйтесь с командой /join.")
        return

    games[chat_id] = {
        "players": [],
        "spy": None,
        "words": random.choice(words),
        "started": False,
        "rounds": 0,
        "spy_wins": 0,
        "citizen_wins": 0,
    }
    await message.reply("🎭 Игра 'Шпион' началась! Присоединяйтесь с командой /join.")
    logger.debug(f"Game started in chat {chat_id}")

# Присоединение к игре
async def join_game(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.first_name

    if chat_id not in games:
        await message.reply("Игра ещё не началась. Напиши /startspy, чтобы начать.")
        return

    if games[chat_id]["started"]:
        await message.reply("Игра уже началась. Подожди следующего раунда!")
        return

    if user_id in [p["id"] for p in games[chat_id]["players"]]:
        await message.reply("Ты уже в игре!")
        return

    games[chat_id]["players"].append({"id": user_id, "name": username})
    
    # Создание инлайн клавиатуры для отображения списка игроков
    keyboard = types.InlineKeyboardMarkup()
    for player in games[chat_id]["players"]:
        keyboard.add(types.InlineKeyboardButton(player["name"], callback_data=f"player_{player['id']}"))
    
    await message.reply(f"{username} присоединился к игре! Всего игроков: {len(games[chat_id]['players'])}.", reply_markup=keyboard)
    logger.debug(f"{username} joined the game in chat {chat_id}")

# Начало раунда
async def start_round(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in games or len(games[chat_id]["players"]) < 3:
        await message.reply("Для начала игры нужно как минимум 3 игрока. Присоединяйтесь с командой /join.")
        return

    if games[chat_id]["started"]:
        await message.reply("Раунд уже начался!")
        return

    games[chat_id]["started"] = True

    # Выбираем шпиона
    players = games[chat_id]["players"]
    spy_index = random.randint(0, len(players) - 1)
    games[chat_id]["spy"] = players[spy_index]["id"]

    # Раздаём слова
    word_for_citizens, word_for_spy = games[chat_id]["words"]
    for player in players:
        word = word_for_spy if player["id"] == games[chat_id]["spy"] else word_for_citizens
        try:
            await bot.send_message(player["id"], f"Твоё слово: {word}")
        except Exception as e:
            logger.error(f"Error sending word to {player['name']}: {e}")
            continue

    # Сообщение в чат
    await message.reply(
        "🔍 Все получили свои слова! Задавайте друг другу вопросы, чтобы найти шпиона. "
        "Шпион должен притворяться, что знает слово. "
        "После обсуждения голосуйте за шпиона с помощью команды /vote @username."
    )

    # Таймер на обсуждение (например, 2 минуты)
    await asyncio.sleep(120)
    if games[chat_id]["started"]:
        await message.reply("Время для обсуждения закончилось! Переходим к голосованию.")
        logger.debug(f"Discussion time ended in chat {chat_id}")

# Голосование
async def vote(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in games or not games[chat_id]["started"]:
        await message.reply("Сейчас нет активного раунда. Напишите /startround, чтобы начать.")
        return

    try:
        voted_username = message.text.split()[1].replace("@", "")
    except IndexError:
        await message.reply("Укажите, за кого голосуете: /vote @username.")
        return

    players = games[chat_id]["players"]
    voted_player = next((p for p in players if p["name"] == voted_username), None)
    if not voted_player:
        await message.reply("Такого игрока нет в игре.")
        return

    if "votes" not in games[chat_id]:
        games[chat_id]["votes"] = {}
    games[chat_id]["votes"][voted_player["id"]] = games[chat_id]["votes"].get(voted_player["id"], 0) + 1

    await message.reply(f"Голос засчитан за {voted_username}!")
    logger.debug(f"Vote recorded for {voted_username} in chat {chat_id}")

    # Проверяем, закончено ли голосование
    if len(games[chat_id]["votes"]) >= len(players):
        await end_round(chat_id)

# Завершение раунда
async def end_round(chat_id):
    players = games[chat_id]["players"]
    spy_id = games[chat_id]["spy"]
    votes = games[chat_id]["votes"]

    # Находим игрока с максимальным количеством голосов
    most_voted = max(votes, key=votes.get)
    spy_found = most_voted == spy_id

    result = "🎉 Шпион пойман!" if spy_found else "😈 Шпион сбежал!"
    await bot.send_message(chat_id, f"{result}\n\nШпионом был(а): {next(p['name'] for p in players if p['id'] == spy_id)}")

    # Обновляем статистику
    if spy_found:
        games[chat_id]["citizen_wins"] += 1
    else:
        games[chat_id]["spy_wins"] += 1

    games[chat_id]["rounds"] += 1

    # Отправляем статистику по завершению игры
    await bot.send_message(chat_id, f"Раунд завершён. Общее количество раундов: {games[chat_id]['rounds']}\n"
                                   f"Шпионов поймано: {games[chat_id]['citizen_wins']}\n"
                                   f"Шпионов сбежало: {games[chat_id]['spy_wins']}")

    # Сбрасываем данные игры
    games.pop(chat_id)
    logger.debug(f"Game ended and reset in chat {chat_id}")

# Статистика игры
async def show_stats(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in games:
        await message.reply("Игра не запущена.")
        return

    stats = games[chat_id]
    await message.reply(f"Статистика игры:\n"
                        f"Общее количество раундов: {stats['rounds']}\n"
                        f"Шпионов поймано: {stats['citizen_wins']}\n"
                        f"Шпионов сбежало: {stats['spy_wins']}")
    logger.debug(f"Statistics sent for chat {chat_id}")

    # Регистрация обработчиков
def register(dp: Dispatcher):
    dp.register_message_handler(start_game, commands=["startspy"])
    dp.register_message_handler(join_game, commands=["join"])
    dp.register_message_handler(start_round, commands=["startround"])
    dp.register_message_handler(vote, commands=["vote"])
    dp.register_message_handler(show_stats, commands=["stats"])
    logging.debug("Модуль spy: успешно настроен.")