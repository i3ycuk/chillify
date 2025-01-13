from brain import dp, types, get_gif, random, Dispatcher, logging

async def send_relax_message(message: types.Message):
    logging.debug(f"Получена команда: {message.text}")
    relax_msg = get_relax_message()
    gif_url = get_gif("relax")
    
    if gif_url:
        await message.reply_animation(gif_url, caption=relax_msg)
    else:
        await message.reply(relax_msg)

relax_messages = [
    "Закрой глаза, сделай глубокий вдох и отпусти все заботы. 🌿",
    "Представь, как ты лежишь на пляже, и волны мягко касаются твоих ног. 🌊",
    "Медленно дыши, отпускай стресс и наполняйся позитивом. 🧘‍♂️"
]

def get_relax_message():
    return random.choice(relax_messages)

def register(dp: Dispatcher):
    dp.register_message_handler(send_relax_message, commands=["relax"])
    logging.debug("Модуль relax: успешно настроен.")