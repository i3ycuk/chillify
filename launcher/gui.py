import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QPlainTextEdit, QMessageBox
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chillify Launcher")

        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)

        self.start_button = QPushButton("Start Bot")
        self.stop_button = QPushButton("Stop Bot")
        self.clear_cache_button = QPushButton("Clear Cache")

        layout = QVBoxLayout()
        layout.addWidget(self.log_widget)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.clear_cache_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_log_message(self, message):
        self.log_widget.appendPlainText(message + "\n")
        self.log_widget.verticalScrollBar().setValue(self.log_widget.verticalScrollBar().maximum()) # Автопрокрутка

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()


class QtHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        message = self.format(record)
        self.widget.add_log_message(message)

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()

    # Настройка логирования для вывода в виджет и файл
    qt_handler = QtHandler(window)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    qt_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('launcher.log', mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(qt_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.INFO)

    return app, window