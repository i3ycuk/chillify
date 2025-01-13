from brain import dp, types, ParseMode, openai, random, Dispatcher, logging

async def send_meme(message: types.Message):
    logging.debug(f"Получена команда: {message.text}")
    meme = get_random_meme()
    await message.reply(meme, parse_mode=ParseMode.MARKDOWN)

# Функция для получения мема через OpenAI
def get_random_meme():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "Ты создаёшь смешные мемы."},
                {"role": "user", "content": "Напиши смешной мем о жизни."}
            ],
            max_tokens=60,
            temperature=0.8

        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"Ошибка при получении мема: {e}")
        memes = [
            "Когда ты осознал, что понедельник снова наступил... 🤦‍♂️",
            "Когда встал с постели, но уже хочешь вернуться. 😴",
            "Когда пытаешься быть взрослым, но внутри ещё ребёнок. 🧸"
        ]
        return random.choice(memes)

def register(dp: Dispatcher):
    dp.register_message_handler(send_meme, commands=["memes"])
    logging.debug("Модуль memes: успешно настроен.")