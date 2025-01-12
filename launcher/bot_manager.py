import logging
import sqlite3
import threading
import time
from datetime import datetime, timedelta
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from brain import dp as brain_dp, bot as brain_bot, register as brain_register
from launcher import utils
from PyQt5.QtWidgets import QMessageBox

# ... (импорты и настройки)

bot_instance = None # Экземпляр бота
bot_task = None # Задача для запуска бота

def start_bot(window):
    global bot_instance, bot_task
    if bot_instance is None:
        bot_instance = brain_bot
        brain_register(brain_dp)
        async def run_bot():
            try:
                await brain_dp.start_polling()
            except Exception as e:
                logging.exception("Bot polling error:")
                window.show_message("Error", f"Bot polling error: {e}", QMessageBox.Critical)
        bot_task = asyncio.ensure_future(run_bot())
        window.start_button.setEnabled(False)
        window.stop_button.setEnabled(True)
        logging.info("Bot started.")
        window.show_message("Success", "Bot started", QMessageBox.Information)
    else:
        window.show_message("Warning", "Bot is already running.", QMessageBox.Warning)


def stop_bot(window):
    global bot_instance, bot_task
    if bot_instance:
        async def shutdown_bot():
            await brain_dp.stop_polling()
            await brain_bot.close()
        asyncio.run(shutdown_bot())
        bot_instance = None
        bot_task = None
        window.start_button.setEnabled(True)
        window.stop_button.setEnabled(False)
        logging.info("Bot stopped.")
        window.show_message("Success", "Bot stopped", QMessageBox.Information)
    else:
        window.show_message("Warning", "Bot is not running.", QMessageBox.Warning)

def clear_cache(window):
    try:
        utils.clear_cache()
        logging.info("Cache cleared manually.")
        window.show_message("Success", "Cache cleared.", QMessageBox.Information)

    except Exception as e:
        logging.error(f"Error clearing cache: {e}")
        window.show_message("Error", f"Error clearing cache: {e}", QMessageBox.Critical)

def cleanup_cache_thread():
    utils.create_cache_table()
    while True:
        utils.cleanup_cache()
        time.sleep(86400) # 24 часа

def start_cache_cleanup():
    threading.Thread(target=cleanup_cache_thread, daemon=True).start()