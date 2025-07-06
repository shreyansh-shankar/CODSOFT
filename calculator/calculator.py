import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
)

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple PyQt6 Calculator")
        self.setGeometry(100, 100, 300, 200)
        self.init_ui()

    def init_ui(self):
        # Input for first number
        self.num1_input = QLineEdit(self)
        self.num1_input.setPlaceholderText("Enter first number")

        # Input for second number
        self.num2_input = QLineEdit(self)
        self.num2_input.setPlaceholderText("Enter second number")

        # Operation selector
        self.operation_box = QComboBox(self)
        self.operation_box.addItems(["Add", "Subtract", "Multiply", "Divide"])

        # Button to perform calculation
        self.calc_button = QPushButton("Calculate", self)
        self.calc_button.clicked.connect(self.calculate)

        # Label to show result
        self.result_label = QLabel("Result will appear here", self)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.num1_input)
        layout.addWidget(self.num2_input)
        layout.addWidget(self.operation_box)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate(self):
        try:
            num1 = float(self.num1_input.text())
            num2 = float(self.num2_input.text())
            operation = self.operation_box.currentText()

            if operation == "Add":
                result = num1 + num2
            elif operation == "Subtract":
                result = num1 - num2
            elif operation == "Multiply":
                result = num1 * num2
            elif operation == "Divide":
                if num2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero.")
                result = num1 / num2

            self.result_label.setText(f"Result: {result:.2f}")
        except ValueError:
            self.result_label.setText("Invalid input. Please enter valid numbers.")
        except ZeroDivisionError as e:
            self.result_label.setText(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
