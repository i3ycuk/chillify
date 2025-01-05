from brain import dp, types, ParseMode, openai, Dispatcher

async def send_quote(message: types.Message):
    print(f"Получена команда: {message.text}")
    quote = get_random_quote()
    await message.reply(quote, parse_mode=ParseMode.MARKDOWN)

# Функция для получения цитаты через OpenAI
def get_random_quote():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Можно выбрать другой движок для генерации
            messages=[
                {"role": "system", "content": "Ты помощник, который генерирует мотивирующие цитаты."},
                {"role": "user", "content": "Напиши мотивирующую цитату."}
            ],
            max_tokens=60,
            temperature=0.7
            
           )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Ошибка при получении цитаты: {e}")
        return "Жизнь слишком коротка, чтобы не наслаждаться каждым моментом. 🌿"

def register(dp: Dispatcher):
    dp.register_message_handler(send_quote, commands=["quotes"])
    print("quotes успешно зарегистрирован.")