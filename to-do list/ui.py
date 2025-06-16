from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt
from logic import TaskManager
import os

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📝 To-Do List")
        self.setGeometry(100, 100, 400, 500)

        self.task_manager = TaskManager()

        self.layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)

        self.input_layout.addWidget(self.task_input)
        self.input_layout.addWidget(self.add_button)

        self.task_list = QListWidget()
        self.task_list.itemChanged.connect(self.toggle_task)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_task)

        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.task_list)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)
        self.load_tasks()

    def add_task(self):
        task_text = self.task_input.text().strip()
        if not task_text:
            QMessageBox.warning(self, "Input Error", "Task cannot be empty.")
            return
        self.task_manager.add_task(task_text)
        self.task_input.clear()
        self.refresh_list()

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No Selection", "Select a task to delete.")
            return
        for item in selected_items:
            self.task_manager.delete_task(item.text())
        self.refresh_list()

    def toggle_task(self, item: QListWidgetItem):
        self.task_manager.toggle_task(item.text())
        self.refresh_list()

    def refresh_list(self):
        self.task_list.clear()
        for task in self.task_manager.tasks:
            item = QListWidgetItem(task['name'])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable)
            item.setCheckState(Qt.CheckState.Checked if task['completed'] else Qt.CheckState.Unchecked)
            
            font = item.font()
            if task['completed']:
                item.setForeground(Qt.GlobalColor.gray)
                font.setStrikeOut(True)
            else:
                font.setStrikeOut(False)
            item.setFont(font)
            
            self.task_list.addItem(item)

    def load_tasks(self):
        self.task_manager.load()
        self.refresh_list()
