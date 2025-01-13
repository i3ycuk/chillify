from brain import dp, types, localization, Dispatcher, logging

async def send_about(message: types.Message):
    logging.debug(f"Получена команда: {message.text}")
    about_text = (localization.get("about_message"))
    await message.reply(about_text)

def register(dp: Dispatcher):
    dp.register_message_handler(send_about, commands=["about"])
    logging.debug("Модуль about: успешно настроен.")