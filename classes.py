from brain import json, StatesGroup, State, logging, os

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
                    logging.error(f"Error loading localization file {filename}: {e}")
        if self.default_lang not in self.localizations:
            logging.critical(f"Default localization '{self.default_lang}' not loaded!")
            raise FileNotFoundError(f"Default localization '{self.default_lang}' not loaded!")

    def set_language(self, lang: str):
        self.lang = lang

    def get(self, key):
        try:
            return self.localizations[self.lang][key]
        except KeyError:
            logging.error(f"Key '{key}' not found in '{self.lang}'. Trying default.")
            try:
                return self.localizations[self.default_lang][key]
            except KeyError:
                logging.error(f"Key '{key}' not found even in default '{self.default_lang}'.")
                return f"{{MISSING_TRANSLATION_{key}}}"

class UserState(StatesGroup):
    waiting_for_preferences = State()