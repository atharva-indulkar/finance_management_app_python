from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QMessageBox
from collections import defaultdict


class ShowRecordWindow(QDialog):
    def __init__(self, details):
        super().__init__()
        self.details = details
        self.names = list(details['expense_name'].values())
        self.types = list(details['expense_type'].values())
        self.amounts = list(details['expense_amount'].values())
        self.dates = list(details['expense_time'].values())
        row_wise_data = list(zip(self.names, self.types, self.amounts, self.dates))
        title_label = QLabel("Expense Record History")
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        summary_button = QPushButton("View Summary")
        summary_button.clicked.connect(self.view_summary)

        self.records_table = QTableWidget()
        self.records_table.setColumnCount(4)
        columns_headers = ('Name', 'Type', 'Amount', 'Date')
        self.records_table.setHorizontalHeaderLabels(columns_headers)
        self.records_table.verticalHeader().setVisible(False)

        for row, data in enumerate(row_wise_data):
            self.records_table.insertRow(row)
            for col, item in enumerate(data):
                self.records_table.setItem(row, col, QTableWidgetItem(str(item)))

        layout = QGridLayout()
        layout.addWidget(title_label, 0, 0, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.records_table, 1, 0, 1, 0)
        layout.addWidget(back_button, 2, 1)
        layout.addWidget(summary_button, 2, 0)
        self.setLayout(layout)

    def go_back(self):
        self.close()

    def view_summary(self):
        # Calculate the total expenses per category
        category_totals = defaultdict(float)
        total_expenses = 0.0

        for i, expense_type in enumerate(self.types):
            category_totals[expense_type] += self.amounts[i]
            total_expenses += self.amounts[i]

        # Find the categories with maximum and minimum totals
        max_category = max(category_totals, key=category_totals.get)
        min_category = min(category_totals, key=category_totals.get)

        # Prepare the message for the popup
        summary_text = f"Category with Maximum Expense: {max_category}\n"
        summary_text += f"Category with Minimum Expense: {min_category}\n"
        summary_text += f"Total Expenses: {total_expenses:.2f}\n\n"

        # Prepare category totals for printing on terminal and also for the popup
        for category, total in category_totals.items():
            summary_text += f"Total for {category}: {total:.2f}\n"
            print(f"Total for {category}: {total:.2f}")  # Print to terminal

        # Display the summary in a message box
        summary_widget = QMessageBox()
        summary_widget.setWindowTitle("Expense Summary")
        summary_widget.setText(summary_text)
        summary_widget.setIcon(QMessageBox.Icon.Information)
        summary_widget.setStandardButtons(QMessageBox.StandardButton.Ok)
        summary_widget.exec()

        # Print max, min category and total expenses to terminal
        print(f"\nCategory with Maximum Expense: {max_category}")
        print(f"Category with Minimum Expense: {min_category}")
        print(f"Total Expenses: {total_expenses:.2f}")
