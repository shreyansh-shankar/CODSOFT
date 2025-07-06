# main.py - Main PyQt6 GUI
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QTabWidget, QMessageBox
)
from contact import Contact
from contact_store import ContactStore

class ContactManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contact Manager")
        self.setGeometry(100, 100, 500, 400)
        self.store = ContactStore()
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_add_tab(), "Add Contact")
        self.tabs.addTab(self.create_view_tab(), "View/Search Contacts")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_add_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        for widget, placeholder in zip(
            [self.name_input, self.phone_input, self.email_input, self.address_input],
            ["Name", "Phone", "Email", "Address"]):
            widget.setPlaceholderText(placeholder)
            layout.addWidget(widget)

        add_btn = QPushButton("Add Contact")
        add_btn.clicked.connect(self.add_contact)
        layout.addWidget(add_btn)

        tab.setLayout(layout)
        return tab

    def create_view_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or phone")
        self.search_input.textChanged.connect(self.search_contacts)

        self.contact_list = QListWidget()
        self.contact_list.itemClicked.connect(self.populate_update_fields)

        self.update_name = QLineEdit()
        self.update_phone = QLineEdit()
        self.update_email = QLineEdit()
        self.update_address = QLineEdit()

        self.update_btn = QPushButton("Update Contact")
        self.update_btn.clicked.connect(self.update_contact)

        self.delete_btn = QPushButton("Delete Contact")
        self.delete_btn.clicked.connect(self.delete_contact)

        layout.addWidget(self.search_input)
        layout.addWidget(self.contact_list)
        for widget in [self.update_name, self.update_phone, self.update_email, self.update_address]:
            layout.addWidget(widget)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.delete_btn)

        tab.setLayout(layout)
        self.load_contacts()
        return tab

    def add_contact(self):
        contact = Contact(
            self.name_input.text(),
            self.phone_input.text(),
            self.email_input.text(),
            self.address_input.text()
        )
        self.store.add_contact(contact)
        QMessageBox.information(self, "Success", "Contact added!")
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.load_contacts()

    def load_contacts(self):
        self.contact_list.clear()
        for contact in self.store.get_all_contacts():
            self.contact_list.addItem(f"{contact.name} | {contact.phone}")

    def search_contacts(self):
        query = self.search_input.text()
        results = self.store.search_contacts(query)
        self.contact_list.clear()
        for contact in results:
            self.contact_list.addItem(f"{contact.name} | {contact.phone}")

    def populate_update_fields(self, item):
        name = item.text().split(" | ")[0]
        contact = next((c for c in self.store.contacts if c.name == name), None)
        if contact:
            self.update_name.setText(contact.name)
            self.update_phone.setText(contact.phone)
            self.update_email.setText(contact.email)
            self.update_address.setText(contact.address)

    def update_contact(self):
        old_name = self.contact_list.currentItem().text().split(" | ")[0]
        new_contact = Contact(
            self.update_name.text(),
            self.update_phone.text(),
            self.update_email.text(),
            self.update_address.text()
        )
        self.store.update_contact(old_name, new_contact)
        QMessageBox.information(self, "Updated", "Contact updated successfully")
        self.load_contacts()

    def delete_contact(self):
        name = self.contact_list.currentItem().text().split(" | ")[0]
        self.store.delete_contact(name)
        QMessageBox.information(self, "Deleted", "Contact deleted successfully")
        self.load_contacts()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = ContactManager()
    manager.show()
    sys.exit(app.exec())
