from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QTextEdit, QLineEdit, QPushButton
from services.crm_service import CRMService

class CRMWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.crm_service = CRMService()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Поле для тегов
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Добавить тег...")
        self.tag_input.returnPressed.connect(self.add_tag)

        # Кнопка добавления тега
        self.add_tag_button = QPushButton("Добавить тег")
        self.add_tag_button.clicked.connect(self.add_tag)

        # Поле для статуса
        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Изменить статус...")
        self.status_input.returnPressed.connect(self.update_status)

        # Кнопка изменения статуса
        self.update_status_button = QPushButton("Изменить статус")
        self.update_status_button.clicked.connect(self.update_status)

        # Список клиентов
        self.client_list = QListWidget()
        self.client_list.itemClicked.connect(self.on_client_selected)

        # Поле для заметок
        self.note_display = QTextEdit()
        self.note_display.setReadOnly(True)

        # Поле для ввода заметки
        self.note_input = QLineEdit()
        self.note_input.returnPressed.connect(self.add_note)

        # Кнопка добавления заметки
        self.add_note_button = QPushButton("Добавить заметку")
        self.add_note_button.clicked.connect(self.add_note)

        layout.addWidget(self.tag_input)
        layout.addWidget(self.add_tag_button)
        layout.addWidget(self.status_input)
        layout.addWidget(self.update_status_button)
        layout.addWidget(self.client_list)
        layout.addWidget(self.note_display)
        layout.addWidget(self.note_input)
        layout.addWidget(self.add_note_button)

        self.setLayout(layout)

        # Загружаем клиентов
        self.load_clients()


    def add_tag(self):
        """Добавить тег."""
        client_name = self.client_list.currentItem().text()
        tag = self.tag_input.text()
        if tag:
            self.crm_service.add_tag(client_name, tag)
            self.tag_input.clear()

    def update_status(self):
        """Изменить статус."""
        client_name = self.client_list.currentItem().text()
        status = self.status_input.text()
        if status:
            self.crm_service.update_status(client_name, status)
            self.status_input.clear()


    def load_clients(self):
        """Загрузить список клиентов."""
        clients = self.crm_service.get_clients()
        for client in clients:
            self.client_list.addItem(client.name)

    def on_client_selected(self, item):
        """Обработчик выбора клиента."""
        self.note_display.clear()
        client_name = item.text()
        notes = self.crm_service.get_notes(client_name)
        for note in notes:
            self.note_display.append(note)

    def add_note(self):
        """Добавить заметку."""
        client_name = self.client_list.currentItem().text()
        note_text = self.note_input.text()
        if note_text:
            self.crm_service.add_note(client_name, note_text)
            self.note_display.append(note_text)
            self.note_input.clear()