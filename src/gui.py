from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QIcon, QFont, QColor
from PyQt6.QtCore import Qt
from interpreter import evaluate  


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator with Variables")
        self.setGeometry(200, 200, 500, 400)

        main_layout = QVBoxLayout()

        # Input field
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter your expression (e.g., x = 5 + 3)")
        self.input_field.setFont(QFont("Menlo", 12))
        self.input_field.returnPressed.connect(self.run_command)
        input_layout.addWidget(self.input_field)

        # Run button
        self.run_button = QPushButton("Run", self)
        self.run_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.run_button.clicked.connect(self.run_command)
        input_layout.addWidget(self.run_button)

        main_layout.addLayout(input_layout)

        # Buttons section
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setStyleSheet("background-color: #f44336; color: white;")
        self.clear_button.clicked.connect(self.clear_input)
        button_layout.addWidget(self.clear_button)

        self.history_button = QPushButton("Show History", self)
        self.history_button.setStyleSheet("background-color: #008CBA; color: white;")
        self.history_button.clicked.connect(self.show_history)
        button_layout.addWidget(self.history_button)

        main_layout.addLayout(button_layout)

        # Output display
        self.output_display = QTextEdit(self)
        self.output_display.setReadOnly(True)
        self.output_display.setFont(QFont("Menlo", 12))
        self.output_display.setStyleSheet("background-color: #f9f9f9; border: 1px solid #ccc;")
        main_layout.addWidget(self.output_display)

        # History display
        self.history_display = QTextEdit(self)
        self.history_display.setReadOnly(True)
        self.history_display.setVisible(False)
        self.history_display.setStyleSheet("background-color: #e0e0e0; border: 1px solid #ccc;")
        main_layout.addWidget(self.history_display)

        self.setLayout(main_layout)

    def run_command(self):
        user_input = self.input_field.text().strip()
        try:
            result = evaluate(user_input)
            if isinstance(result, str) and result.startswith("Error"):
                # Display errors
                self.display_output(result, "error")
            elif "=" in user_input:
                # Handle variable assignments
                self.display_output(f"Variable Set: {user_input}", "success")
            elif user_input.startswith("print(") and user_input.endswith(")"):
                # Format print statements
                variable_name = user_input[6:-1].strip()  # Extract the variable name
                self.display_output(f"Expression: {user_input}\nResult: {result}", "result")
            else:
                # Handle standalone variables and expressions
                self.display_output(f"Expression: {user_input}\nResult: {result}", "result")
            # Save the command and result to history
            self.save_to_history(user_input, result)
        except Exception as e:
            # Handle unexpected errors
            self.display_output(f"Error: {e}", "error")
        finally:
            # Clear the input field
            self.input_field.clear()

    def display_output(self, message, message_type):
        color = {"success": "green", "result": "blue", "error": "red"}.get(message_type, "black")
        self.output_display.setTextColor(QColor(color))
        self.output_display.append(message)
        self.output_display.setTextColor(QColor("black"))

    def clear_input(self):
        self.input_field.clear()
        self.output_display.clear()

    def show_history(self):
        self.history_display.setVisible(not self.history_display.isVisible())
        self.history_button.setText(
            "Hide History" if self.history_display.isVisible() else "Show History"
        )

    def save_to_history(self, user_input, result):
        formatted_entry = f">>> {user_input}\n=> {result}\n"
        self.history_display.append(formatted_entry)


if __name__ == "__main__":
    app = QApplication([])
    calculator = CalculatorApp()
    calculator.show()
    app.exec()
