from brain import dp, types, localization, Dispatcher, logging

async def send_help(message: types.Message):
    logging.debug(f"Получена команда: {message.text}")
    help_text = (localization.get("help_message"))
    await message.reply(help_text)

def register(dp: Dispatcher):
    dp.register_message_handler(send_help, commands=["help"])
    logging.debug("Модуль help: успешно настроен.")