import json
import os

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, \
    QListWidget, QDialog, QFileDialog, QMessageBox
from src.contact_dialog import ContactDialog
from src.utils import get_contact_string


class PhoneBookApp(QWidget):
    def __init__(self):
        super().__init__()

        self.contacts = []
        self.current_index = None
        self.file_path = "phone_book.json"

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.contact_list_label = QLabel("Список контактов:")
        self.layout.addWidget(self.contact_list_label)

        self.contact_list = QListWidget()
        self.layout.addWidget(self.contact_list)

        self.search_label = QLabel("Поиск:")
        self.layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.search_contacts)
        self.layout.addWidget(self.search_button)

        self.add_button = QPushButton("Добавить контакт")
        self.add_button.clicked.connect(self.show_add_dialog)
        self.layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Редактировать контакт")
        self.edit_button.clicked.connect(self.show_edit_dialog)
        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить контакт")
        self.delete_button.clicked.connect(self.delete_contact)
        self.layout.addWidget(self.delete_button)

        self.export_button = QPushButton("Экспорт в файл")
        self.export_button.clicked.connect(self.export_data)
        self.layout.addWidget(self.export_button)

        self.import_button = QPushButton("Импорт из файла")
        self.import_button.clicked.connect(self.import_data)
        self.layout.addWidget(self.import_button)

        self.current_file_label = QLabel(f"Текущий файл: {self.file_path}")
        self.layout.addWidget(self.current_file_label)

        self.setStyleSheet('''
            * {
                font-size: 16px;
            }

            PhoneBookApp {
                background-color: #F5F5F5;
            }

            QLabel {
                font-weight: bold;
                color: #4A4A4A;
            }

            QListWidget {
                background-color: #FFFFFF;
                border: 1px solid #D1D1D1;
                color: #333333;
            }

            QListWidget::item {
                padding: 10px;
            }

            QLineEdit {
                border: 2px solid #BDBDBD;
                background-color: #F0F0F0;
                color: #333333;
                padding: 8px;
            }

            QPushButton {
                margin-top: 5px;
                border: 2px solid #6D7B8D;
                background-color: #6D7B8D;
                color: #FFFFFF;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: #546E7A;
            }

            QListWidget::item:selected {
                background-color: #6D7B8D;
                color: #FFFFFF;
            }
        ''')
        
        self.setLayout(self.layout)
        self.setWindowTitle("Телефонный справочник")

        self.update_contact_list()

    def show_add_dialog(self):
        dialog = ContactDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            contact = dialog.get_contact()
            self.contacts.append(contact)
            self.save_data()
            self.update_contact_list()

    def show_edit_dialog(self):
        selected_item = self.contact_list.currentItem()
        if selected_item:
            index = self.contact_list.row(selected_item)
            self.current_index = index

            contact = self.contacts[index]
            dialog = ContactDialog(self, contact)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                updated_contact = dialog.get_contact()
                self.contacts[index] = updated_contact
                self.save_data()
                self.update_contact_list()

    def delete_contact(self):
        selected_item = self.contact_list.currentItem()
        if selected_item:
            index = self.contact_list.row(selected_item)
            del self.contacts[index]
            self.save_data()
            self.update_contact_list()

    def update_contact_list(self, contacts=None):
        self.contact_list.clear()

        if contacts is None:
            contacts = self.contacts

        for contact in contacts:
            self.contact_list.addItem(get_contact_string(contact))

    def search_contacts(self):
        search_text = self.search_input.text().lower()

        if search_text:
            filtered_contacts = [contact for contact in self.contacts if
                                 search_text in get_contact_string(contact).lower()]
            self.update_contact_list(filtered_contacts)
        else:
            self.update_contact_list(self.contacts)

    def process_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                imported_contacts = json.load(file)
                self.contacts = imported_contacts
                self.current_file_label.setText(f"Текущий файл: {os.path.basename(file_path)}")
                self.update_contact_list()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            error_message = f"Произошла ошибка: {str(e)}"
            self.show_error_message(error_message)

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.contacts, file)

    def import_data(self):
        import_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл для импорта", "", "JSON Files (*.json)")

        if import_path:
            try:
                with open(import_path, "r") as file:
                    imported_contacts = json.load(file)
                    self.contacts = imported_contacts
                    self.file_path = import_path
                    self.current_file_label.setText(f"Текущий файл: {os.path.basename(self.file_path)}")
                    self.update_contact_list()
            except Exception as e:
                error_message = f"Ошибка при импорте данных: {str(e)}"
                self.show_error_message(error_message)

    def export_data(self):
        export_path, _ = QFileDialog.getSaveFileName(self, "Выберите файл для экспорта", "", "JSON Files (*.json)")

        if export_path:
            with open(export_path, "w") as file:
                json.dump(self.contacts, file)

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setText("Ошибка")
        error_box.setInformativeText(message)
        error_box.exec_()
