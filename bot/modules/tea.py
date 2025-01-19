from brain import random, asyncio, types, InlineKeyboardMarkup, InlineKeyboardButton, logging

def register(dp):
    @dp.message_handler(lambda message: message.text and message.text.strip().lower() in ["чай", "цай"])
    async def make_tea(message: types.Message):
        username = message.from_user.first_name or message.from_user.username or "друг чая"

        # Создание инлайн-кнопок для выбора чая
        tea_keyboard = InlineKeyboardMarkup(row_width=2)
        tea_keyboard.add(
            InlineKeyboardButton("1️⃣ Черный чай", callback_data="tea_black"),
            InlineKeyboardButton("2️⃣ Зеленый чай", callback_data="tea_green"),
            InlineKeyboardButton("3️⃣ Мятный чай", callback_data="tea_mint"),
            InlineKeyboardButton("4️⃣ Чайный набор (с чаем и сладостями)", callback_data="tea_full")
        )

        # Приветствие и предложение выбора чая
        await message.reply(
            f"🫖 Привет, {username}! Сейчас я приготовлю тебе особенный азербайджанский чай. Какой вид предпочитаешь?",
            reply_markup=tea_keyboard
        )

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("tea_"))
    async def tea_selection(callback_query: types.CallbackQuery):
        tea_types = {
            "tea_black": "черный чай",
            "tea_green": "зеленый чай",
            "tea_mint": "мятный чай",
            "tea_full": "чайный набор (с чаем и сладостями)"
        }
        tea_type = tea_types.get(callback_query.data, "чай")

        username = callback_query.from_user.first_name or callback_query.from_user.username or "друг чая"

        # Пошаговое заваривание чая
        steps = [
            f"🍃 {username}, выбираю самые качественные чайные листья...",
            "🍵 Ополаскиваю чайник горячей водой, чтобы чай был вкуснее...",
            "🔥 Вода кипит, комната наполняется ароматом азербайджанского чая...",
            f"✨ Завариваю {tea_type} с любовью и теплыми чувствами для тебя...",
            "⏳ Ждём, пока чай заварится, чтобы вкус стал насыщеннее...",
            f"🫖 Чай готов! Разливаю его в стаканы с тонким стеклом."
        ]

        for step in steps:
            await callback_query.message.answer(step)
            await asyncio.sleep(2)

        # Советы для идеального чаепития
        tea_tips = [
            "🍯 Добавь немного мёда в чай, это очень полезно для здоровья.",
            "🍋 Долька лимона сделает чай более освежающим.",
            "🍪 Сладости, такие как шакербура и пахлава, идеально подходят к чаю.",
            "🎶 Слушай свою любимую музыку во время чаепития, и удовольствие удвоится."
        ]

        # Эмоциональное завершение
        warm_message = (
            f"🥰 Вот твой {tea_type}, {username}! Пей чай с мёдом, лимоном или сладостями. "
            "Желаю тебе уюта и хорошего настроения. Если захочешь поговорить, я всегда рядом. 🌟"
        )
        await callback_query.message.answer(warm_message)

        encouragements = [
            "🌼 В каждой трудности есть своя отрада.",
            "🌞 Всё будет хорошо, даже если сегодня кажется иначе.",
            "🍂 Иногда лучший ответ — это пауза с чашкой чая.",
            "✨ Ты очень ценен, не забывай об этом."
        ]

        # Итоговое сообщение с рандомным советом и пожеланием
        final_message = (
            f"💡 Совет: {random.choice(tea_tips)}\n"
            f"✨ {random.choice(encouragements)}"
        )
        await callback_query.message.answer(final_message)

logging.debug("Модуль tea: успешно настроен.")