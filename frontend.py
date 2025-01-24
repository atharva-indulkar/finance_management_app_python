from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (QMainWindow, QLabel, QWidget, QGridLayout, QPushButton, QMessageBox, QDialog,
                             QLineEdit, QComboBox, QCalendarWidget)
from show_record_file import ShowRecordWindow
from expense_class import ExpenseDetails
from expense_class import ShowingDetails
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Management App")
        title_label = QLabel("Finance Management App")
        show_expense_window_button = QPushButton("Show Expense Records")
        show_expense_window_button.clicked.connect(self.show_expense_window)
        log_expense_window_button = QPushButton("Log new Expense")
        log_expense_window_button.clicked.connect(self.log_expense_window)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close_window)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QGridLayout()
        layout.addWidget(title_label, 0, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(show_expense_window_button, 1, 0)
        layout.addWidget(log_expense_window_button, 1, 1)
        layout.addWidget(exit_button, 2, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.centralWidget.setLayout(layout)

    def log_expense_window(self):
        log_expense_window = LogExpenseWindow()
        log_expense_window.exec()


    def show_expense_window(self):
        showing_details = ShowingDetails()
        details = showing_details.show_expense()
        show_record_window = ShowRecordWindow(details)
        show_record_window.exec()

    def close_window(self):
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Close Window ?")
        confirmation_widget.setText("Are you sure you want to exit the app ?")
        confirmation_widget.setIcon(QMessageBox.Icon.Question)
        confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        confirm = confirmation_widget.exec()
        if confirm == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            confirmation_widget.close()


class LogExpenseWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.pop_up_of_non_numeric = False
        expense_label = QLabel("Log new expense")
        name_label = QLabel('Name')
        type_label = QLabel('Type')
        amount_label = QLabel('Amount')
        date_label = QLabel('Select Date')
        self.name_input = QLineEdit()  #Everything which the user will input will be "self" as everytime, the input will be different
        self.name_input.setToolTip('Give name of the expense, Eg: Crocin')
        self.type_input = QComboBox()
        expense_type_list = ['Education', 'Travel', 'Groceries', 'Rent', 'Utilities', 'Investments', 'Medical',
                             'Pharmaceuticals',
                             'Maintenance', 'Taxes', 'Loan EMIs', 'Hygiene', 'Entertainment', 'Food',
                             'Vacation(Holidays)',
                             'Fashion', 'Shopping', 'Self care', 'Misc']
        self.amount_input = QLineEdit()
        self.amount_input.setToolTip('Give amount only in numeric value, Eg:5005.23')
        self.type_input.addItems(expense_type_list)
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMaximumDate(QDate.currentDate())
        log_expense_button = QPushButton('Record Expense')
        log_expense_button.clicked.connect(self.log_expense)
        layout = QGridLayout()
        layout.addWidget(expense_label, 0, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label, 1, 0)
        layout.addWidget(self.name_input, 1, 1)
        layout.addWidget(type_label, 2, 0)
        layout.addWidget(self.type_input, 2, 1)
        layout.addWidget(amount_label, 3, 0)
        layout.addWidget(self.amount_input, 3, 1)
        layout.addWidget(date_label, 4, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.calendar, 5, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(log_expense_button, 6, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def log_expense(self):
        name = self.name_input.displayText()
        amount = self.amount_input.displayText()
        try:
            amount = float(amount)
        except ValueError:
            self.amount_input.clear()
            amount = 0.0
            self.pop_up_of_non_numeric = True
            if len(name) != 0:
                warning_widget = QMessageBox()
                warning_widget.setWindowTitle("Unacceptable input")
                warning_widget.setText("Please enter numeric value")
                warning_widget.setIcon(QMessageBox.Icon.Warning)
                warning_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
                confirm = warning_widget.exec()
                if confirm == QMessageBox.StandardButton.Ok:
                    warning_widget.close()
            if len(name.strip()) == 0:
                self.pop_up_of_non_numeric = False
        type_exp = self.type_input.currentText()
        date = self.calendar.selectedDate().toString()
        if len(name.strip()) != 0 and amount > 0:
            expense_details = ExpenseDetails(
                name=name,
                type_exp=type_exp,
                amount=amount,
                date=date
            )
            expense_details.log_expense()
            del expense_details
            confirmation_widget = QMessageBox()
            confirmation_widget.setWindowTitle("Success")
            confirmation_widget.setText("Expense Logged Successfully\n"
                                        "Do you want to log a new expense")
            confirmation_widget.setIcon(QMessageBox.Icon.Question)
            confirmation_widget.setStandardButtons(QMessageBox.StandardButton.Yes |
                                                   QMessageBox.StandardButton.No)
            confirm = confirmation_widget.exec()
            if confirm == QMessageBox.StandardButton.Yes:
                self.amount_input.clear()
                self.name_input.clear()
                confirmation_widget.close()
            else:
                confirmation_widget.close()
                self.close()

        else:
            if not self.pop_up_of_non_numeric:
                warning_widget = QMessageBox()
                warning_widget.setWindowTitle("Unacceptable input")
                warning_widget.setText("Please check data.Some of the input field may be empty")
                warning_widget.setIcon(QMessageBox.Icon.Warning)
                warning_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
                confirm = warning_widget.exec()
                if confirm == QMessageBox.StandardButton.Ok:
                    warning_widget.close()
