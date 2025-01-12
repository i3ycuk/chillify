import logging, sqlite3, asyncio, json, random, os, importlib, openai, requests, sys, subprocess, dominate, datetime, psycopg2, threading, time, telethon

from datetime import timedelta, timezone
from telethon import TelegramClient, events, sync, errors, utils
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.sessions import StringSession
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QPlainTextEdit, QMessageBox, QLineEdit, QTabWidget, QLabel, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, QTimer
from aiogram import Bot, Dispatcher, types, executor, exceptions
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked, MessageToDeleteNotFound, MessageCantBeDeleted
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from collections import defaultdict
from locales.languages import LANGUAGES_PER_PAGE, LANGUAGES, LANGUAGES_TRANSLATIONS, LANGUAGES_FLAGS
from dotenv import load_dotenv
from config import API_TOKEN, OPENAI_API_KEY, GIPHY_API_KEY, DB_SETTINGS, API_ID, API_HASH, DATABASE_FILE, CACHE_EXPIRATION_TIME, PHONE_NUMBER, LOG_FILE, LOG_LEVEL
from client.utils import create_cache_table, cleanup_cache, store_message_data, get_message_data, delete_message_data
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

from logs import log_stream, error_handler, logger, message_cache, clear_cache_daily, safe_delete_message
from handlers.giphy import get_gif
from handlers.quotes import get_random_quote
from handlers.memes import get_random_meme
from handlers.relax import get_relax_message
