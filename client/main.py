from pathlib import Path
import sys
import subprocess
import logging
from PyQt5.QtWidgets import QApplication
#from frontend.main_window import MainWindow

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    # Запуск графического интерфейса
    app = QApplication(sys.argv)
    #window = MainWindow()
    #window.show()

    # Добавляем корень проекта в sys.path
    project_root = Path(__file__).resolve().parent.parent  # Переход на два уровня вверх
    sys.path.append(str(project_root))

    # Запуск бота через subprocess
    try:
        subprocess.Popen([sys.executable, "bot/main.py"])
        logging.info("Клиент успешно запущен.")
    except Exception as e:
        logging.error(f"Ошибка при запуске клиента: {e}")

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()