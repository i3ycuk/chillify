import logging, sqlite3, asyncio, json, random, os, importlib, openai, requests, sys, subprocess, dominate, datetime, psycopg2

from aiogram import Bot, Dispatcher, types, executor, exceptions
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked, MessageToDeleteNotFound, MessageCantBeDeleted
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from collections import defaultdict
from locales.languages import LANGUAGES_PER_PAGE, LANGUAGES, LANGUAGES_TRANSLATIONS, LANGUAGES_FLAGS
from dotenv import load_dotenv
from config import API_TOKEN, OPENAI_API_KEY, GIPHY_API_KEY, DB_SETTINGS
from functools import partial

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
openai.api_key = OPENAI_API_KEY
message_cache = defaultdict(dict)

from psycopg2 import sql
from dominate.tags import html, head, title, body, h1, p, pre, footer, style
from io import StringIO
from typing import Optional
from database import get_user_language, create_db, add_user, connect_db, get_user, update_user_messages
from classes import *

localization = Localization()

from logs import *
from handlers.giphy import get_gif
from handlers.quotes import get_random_quote
from handlers.memes import get_random_meme
from handlers.relax import get_relax_message
