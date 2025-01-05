from brain import json, StatesGroup, State, logging

class Localization:
    class LocalizationKeyNotFound(Exception):
        pass

    def __init__(self, default_lang: str = "en"): # ������������ ��� �������
        self.default_lang = default_lang # ��������� ���� �� ���������
        self.lang = None # ���������� ���� �� ����������
        self.localizations = {}

    def load_localizations(self):
        lang_to_load = self.lang or self.default_lang # ��������� ������� ��� ���������
        try:
            with open(f"locales/{lang_to_load}.json", "r", encoding="utf-8-sig") as file:
                self.localizations = json.load(file)
        except FileNotFoundError:
            if lang_to_load != self.default_lang: # ���� �� ������� ��������� �������, ������� ���������
                logging.warning(f"Localization file for language '{lang_to_load}' not found. Using default '{self.default_lang}' localization.")
                self.lang = self.default_lang
                self.load_localizations() # ����������� �����
                return
            else:
                logging.critical(f"Default '{self.default_lang}' localization file not found! Bot cannot start.")
                raise
        except json.JSONDecodeError as e:
            if lang_to_load != self.default_lang:
                logging.critical(f"Error decoding JSON in localization file for '{lang_to_load}': {e}. Trying default.")
                self.lang = self.default_lang
                self.load_localizations()
                return
            else:
                logging.critical(f"Error decoding JSON in default localization file '{self.default_lang}': {e}")
                raise

    def get(self, key):
        try:
            return self.localizations[self.lang][key]
        except KeyError:
            logging.error(f"Key '{key}' not found in localization for language '{self.lang}'.")
            try:
                return self.localizations[self.default_lang][key]
            except KeyError:
                logging.error(f"Key '{key}' not found even in default localization '{self.default_lang}'.")
                return f"{{MISSING_TRANSLATION_{key}}}" # ����� ������������� �������

    def set_language(self, lang: str):
        if self.lang != lang: # ��������� ������ ���� ���� ���������
            self.lang = lang
            self.load_localizations()

class UserState(StatesGroup):
    waiting_for_preferences = State()