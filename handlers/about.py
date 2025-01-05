from brain import dp, types, localization, Dispatcher

async def send_about(message: types.Message):
    print(f"ѕолучена команда: {message.text}")
    about_text = (localization.get("about_message"))
    await message.reply(about_text)

def register(dp: Dispatcher):
    dp.register_message_handler(send_about, commands=["about"])
    print("about успешно зарегистрирован.")