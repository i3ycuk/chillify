import asyncio
import logging
import random

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BadRequest, TelegramAPIError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# Константы для анимаций
ANIMATIONS = [
    ["", "‍♂️", "", ""],  # Идущий человечек
    ["", "", "", "", "", "", "", ""],  # Луна
    ["⏳", "⌛"],  # Песочные часы
    ["", "✨", "", ""],  # Вихрь/звезды
    ["(¬‿¬)", "(¬‿¬)", "(͡° ͜ʖ ͡°)", "(¬‿¬)"],  # Танцор
    ["", "‍➡️", "", "‍♂️"],  # Бегущий человек
    ["", "", ""],  # Растущее дерево
    ["", "♨️", ""],  # Огонь
    ["️", "", "️"],  # Ветер
    ["️", "⛈️", "️"],  # Дождь
    ["", "", "", "", ""],  # Машины
    ["⚽", "", "", "⚾", ""], #спортивные мячи
    ["", "", ""], #Лампочка
    ["", "⚙️", "⚙️"], #Шестеренки
    ["", "", ""], #Молоток
    ["", "⏳", "⌛", "⏳"], #Более длинные песочные часы
    ["⬆️","⬇️"], #Стрелки вверх вниз
    ["⏪","▶️","⏩"], #Кнопки плеера
    ["","","️"] #Облачка мыслей
]

# Случайные поводы для собраний (расширено)
MEETING_REASONS = [
    "Обсуждение экзистенциального смысла бытия.",
    "Собрание по вопросу о том, почему коты так любят коробки.",
    "Внеплановое совещание по распределению ролей в грядущем зомби-апокалипсисе.",
    "Сеанс одновременной медитации на тему поиска потерянного носка.",
    "Круглый стол по обмену лучшими мемами за неделю.",
    "Стратегическая сессия по захвату мира (начнем с соседнего подъезда).",
    "Разбор полетов после вчерашнего чаепития.",
    "Собрание тайного ордена любителей пиццы с ананасами (или без).",
    "Экстренное совещание по решению проблемы переполнения чата котиками.",
    "Обсуждение влияния фазы луны на количество багов в коде.",
    "Разбор полётов на ковре-самолёте.",
    "Собрание по переименованию единорогов в радужных коней.",
    "Обсуждение этикета поедания супа вилкой.",
    "Важное совещание по определению лучшего сорта пельменей.",
    "Круглый стол по вопросам межгалактического этикета.",
    "Собрание по обсуждению теории струн (без струн).",
    "Экстренное совещание по поиску пропавшего пульта от телевизора.",
    "Семинар по эффективному использованию силы мысли для поиска ключей.",
    "Обсуждение влияния параллельных вселенных на утренний кофе.",
    "Конференция по вопросам перемещения во времени с помощью стиральной машины."
]

# Случайные метафизические/смешные сообщения (расширено)
MESSAGES = [
    "Внезапно, реальность начала мерцать...",
    "Кажется, кто-то уронил пространственно-временной континуум.",
    "Вселенная пытается отправить нам сообщение... возможно, это спам.",
    "Мы собрались здесь, чтобы разгадать загадку курицы и яйца... снова.",
    "Поговаривают, что за этим собранием наблюдают высшие силы... или просто соседский кот.",
    "Сегодня мы откроем портал... в мир бесконечного печенья.",
    "Внимание! Возможно временное искажение реальности. Не теряйте носки.",
    "Мы собрались, чтобы обсудить, что было раньше: пицца или ананас.",
    "Сегодня мы постигнем тайну исчезновения носков в стиральной машине.",
    "Мы здесь, чтобы найти ответ на главный вопрос жизни, вселенной и всего остального... и это 42.",
    "Говорят, здесь можно найти ответы на все вопросы... или хотя бы на один.",
    "Мы собрались, чтобы пересмотреть законы гравитации. Кто принёс батут?",
    "Сегодня мы будем искать философский камень... в холодильнике.",
    "Пространство и время – это всего лишь иллюзия... особенно по утрам.",
    "Наше собрание проходит под эгидой борьбы с гравитацией и здравым смыслом.",
    "Внимание! Возможны побочные эффекты в виде внезапного просветления или желания танцевать.",
    "Мы здесь, чтобы доказать, что коты – это на самом деле инопланетяне.",
    "Сегодня мы будем изучать телепортацию с помощью микроволновки (не повторять дома!).",
    "Мы собрались, чтобы обсудить, как заставить время идти медленнее по понедельникам."
]


async def summon_handler(message: types.Message):
    """Обработчик 'созвать всех' с анимацией и уведомлением причины."""

    if not isinstance(message.chat, types.Chat):
        try:
            await message.reply("Эта команда работает только в группах и каналах.")
        except TelegramAPIError as e:
            logging.error(f"Telegram API Error (Reply): {e}")
        return

    chat_id = message.chat.id
    bot = message.bot
    summon_message = message.get_args() or "Созываем всех!"

    members_ids = []
    try:
        if message.chat.type in ["group", "supergroup"]:
            try:
                members = await bot.get_chat_administrators(chat_id)
                members_ids = [member.user.id for member in members if member.status not in ["left", "kicked"]]
            except (BadRequest, TelegramAPIError) as e:
                logging.error(f"Error getting chat administrators: {e}")
                try:
                    await message.reply("Произошла ошибка при получении списка участников.")
                except TelegramAPIError as e:
                    logging.error(f"Telegram API Error (Reply): {e}")
                return

        elif message.chat.type == "channel":
            from brain import client
            if not (client and client.is_connected()):
                try:
                    await message.reply("Необходимо подключиться к Telegram через клиент для использования этой команды в каналах.")
                except TelegramAPIError as e:
                    logging.error(f"Telegram API Error (Reply): {e}")
                return

            offset = 0
            limit = 100
            all_participants = []
            try:
                while True:
                    participants = await client(GetParticipantsRequest(
                        channel=chat_id,
                        filter=ChannelParticipantsSearch(''),
                        offset=offset,
                        limit=limit,
                        hash=0
                    ))
                    if not participants.users:
                        break
                    all_participants.extend(participants.users)
                    offset += len(participants.users)
                members_ids = [user.id for user in all_participants]
            except TelegramAPIError as e:
                logging.error(f"Telethon error getting participants: {e}")
                try:
                    await message.reply("Ошибка при получении участников канала.")
                except TelegramAPIError as e:
                    logging.error(f"Telegram API Error (Reply): {e}")
                return

        else:
            try:
                await message.reply("Эта команда работает только в группах и каналах.")
            except TelegramAPIError as e:
                logging.error(f"Telegram API Error (Reply): {e}")
            return

        if not members_ids:
            try:
                await message.reply("В этом чате нет участников.")
            except TelegramAPIError as e:
                logging.error(f"Telegram API Error (Reply): {e}")
            return

        sent_message = None
        try:
            sent_message = await bot.send_message(chat_id, f"{summon_message}\n\n", parse_mode=types.ParseMode.MARKDOWN)

            if ANIMATIONS:
                chosen_animation = random.choice(ANIMATIONS)
                animation_text = f"{summon_message}\n\n"
                for frame in chosen_animation:
                    try:
                        await sent_message.edit_text(animation_text + frame)
                        await asyncio.sleep(0.3)
                    except TelegramAPIError as e:
                        logging.error(f"Telegram API Error during animation: {e}")
                        break
            else:
                logging.warning("No animations available. Skipping animation.")

            await asyncio.sleep(30)

            reason = random.choice(MEETING_REASONS)
            message_after_delay = random.choice(MESSAGES)

            mentions = [f"[{user_id}](tg://user?id={user_id})" for user_id in members_ids]
            notification_message = f" Внимание! Собрание по причине:\n*{reason}*\n{message_after_delay}\n\nУчастники: {' '.join(mentions)}"
            await bot.send_message(chat_id, notification_message, parse_mode=types.ParseMode.MARKDOWN)

            try:
                await message.delete()
                if sent_message:
                    await bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)
            except TelegramAPIError as e:
                logging.error(f"Telegram API Error (Delete): {e}")

        except TelegramAPIError as e:
            logging.error(f"Telegram API Error (main part): {e}")
        except Exception as e:
            logging.exception(f"Unexpected error in summon_handler: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error in summon_handler (outer): {e}")

def register(dp: Dispatcher):
    dp.register_message_handler(summon_handler, Text(equals=["созвать всех", "тег всех"], ignore_case=True))
    logging.debug("Модуль summon: успешно настроен.")