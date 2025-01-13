from brain import json, StatesGroup, State, logging, os, get_user_language, BaseMiddleware, types, dp

class LocalizationMiddleware(BaseMiddleware):
    async def __call__(self, handler, update: types.Update, data: dict):
        user_id = update.message.from_user.id if update.message else update.callback_query.from_user.id
        language = get_user_language(user_id) or "en"
        data["language"] = language
        logging.debug(f"Вывод языка в data: {data}")  # Print data for debugging
        return await handler(update, data)

# Registration remains the same
dp.middleware.setup(LocalizationMiddleware())

class Localization:
    def __init__(self, default_lang: str = "en"):
        self.default_lang = default_lang
        self.lang = None
        self.localizations = {}
        self.load_all_localizations()

    def load_all_localizations(self):
        locales_dir = "locales"
        for filename in os.listdir(locales_dir):
            if filename.endswith(".json"):
                lang_code = filename[:-5]
                try:
                    with open(os.path.join(locales_dir, filename), "r", encoding="utf-8-sig") as file:
                        self.localizations[lang_code] = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    logging.error(f"Ошибка загрузки файла локализации {filename}: {e}")
        if self.default_lang not in self.localizations:
            logging.critical(f"Файл локализации по умолчанию '{self.default_lang}' не загружен!")
            raise FileNotFoundError(f"Файл локализации по умолчанию '{self.default_lang}' не загружен!")

    def set_language(self, lang: str):
        self.lang = lang

    def get(self, key):
        try:
            return self.localizations[self.lang][key]
        except KeyError:
            logging.error(f"Ключ локализации '{key}' не найден в '{self.lang}'. попытка установить язык по умолчанию.")
            try:
                return self.localizations[self.default_lang][key]
            except KeyError:
                logging.error(f"Ключ локализации по умолчанию '{key}' не найден в '{self.default_lang}'.")
                return f"{{MISSING_TRANSLATION_{key}}}"

class UserState(StatesGroup):
    waiting_for_preferences = State()