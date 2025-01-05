from brain import dp, types, localization, Dispatcher

async def send_help(message: types.Message):
    print(f"ѕолучена команда: {message.text}")
    help_text = (localization.get("help_message"))
    await message.reply(help_text)

def register(dp: Dispatcher):
    dp.register_message_handler(send_help, commands=["help"])
    print("help успешно зарегистрирован.")