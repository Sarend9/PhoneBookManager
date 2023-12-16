import sys
from PySide2.QtWidgets import QApplication

from src.phonebook_app import PhoneBookApp

if __name__ == '__main__':
    app = QApplication([])
    phone_book_app = PhoneBookApp()
    phone_book_app.show()
    sys.exit(app.exec_())
