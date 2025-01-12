import sys
from PyQt5.QtWidgets import QApplication
from gui import run_gui, MainWindow
import bot_manager
import logging

if __name__ == "__main__":
    app, window = run_gui()
    bot_manager.start_cache_cleanup() # Запуск очистки кэша

    window.start_button.clicked.connect(lambda: bot_manager.start_bot(window)) # Передача окна
    window.stop_button.clicked.connect(lambda: bot_manager.stop_bot(window))
    window.clear_cache_button.clicked.connect(lambda: bot_manager.clear_cache(window))

    window.show()
    sys.exit(app.exec_())