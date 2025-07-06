# contact_store.py - Manages contact storage and basic CRUD operations
import json
import os
from contact import Contact

class ContactStore:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.contacts = [Contact.from_dict(d) for d in data]

    def save_contacts(self):
        with open(self.filename, "w") as f:
            json.dump([c.to_dict() for c in self.contacts], f, indent=4)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def delete_contact(self, name):
        self.contacts = [c for c in self.contacts if c.name != name]
        self.save_contacts()

    def update_contact(self, old_name, updated_contact):
        for idx, contact in enumerate(self.contacts):
            if contact.name == old_name:
                self.contacts[idx] = updated_contact
                break
        self.save_contacts()

    def search_contacts(self, query):
        return [c for c in self.contacts if query.lower() in c.name.lower() or query in c.phone]

    def get_all_contacts(self):
        return self.contacts