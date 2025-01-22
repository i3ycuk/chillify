from PyQt5.QtWidgets import QMainWindow, QTabWidget
from frontend.chat_window import ChatWindow
from frontend.crm_window import CRMWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Clone")
        self.setGeometry(100, 100, 800, 600)

        # —оздаем вкладки
        self.tabs = QTabWidget()
        self.tabs.addTab(ChatWindow(), "„аты")
        self.tabs.addTab(CRMWindow(), "CRM")

        self.setCentralWidget(self.tabs)