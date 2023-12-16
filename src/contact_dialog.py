from PySide2.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from src.utils import create_contact


class ContactDialog(QDialog):
    def __init__(self, parent, contact=None):
        super().__init__(parent)

        self.contact = contact

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.phone_number_input = QLineEdit()

        self.layout.addWidget(QLabel("Имя:"))
        self.layout.addWidget(self.first_name_input)

        self.layout.addWidget(QLabel("Фамилия:"))
        self.layout.addWidget(self.last_name_input)

        self.layout.addWidget(QLabel("Телефон:"))
        self.layout.addWidget(self.phone_number_input)

        self.buttons_layout = QVBoxLayout()

        self.ok_button = QPushButton("ОК")
        self.ok_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

        if self.contact:
            self.first_name_input.setText(self.contact["first_name"])
            self.last_name_input.setText(self.contact["last_name"])
            self.phone_number_input.setText(self.contact["phone_number"])

    def get_contact(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone_number = self.phone_number_input.text()

        return create_contact(first_name, last_name, phone_number)
