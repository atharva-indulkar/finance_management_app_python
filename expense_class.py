import os.path
import pandas as pd


class ExpenseDetails:
    def __init__(self, name, type_exp, amount, date):
        self.read_df = None
        self.file_name = 'expense_records.csv'
        self.expense_name = name
        self.expense_type = type_exp
        self.expense_amount = amount
        self.expense_date = date
        self.expense_details = {  # Initialized a dictionary to store expense details.
            'expense_name': [],
            'expense_type': [],
            'expense_amount': [],
            'expense_time': [],
        }
        self.df = None

    def log_expense(self):
        self.expense_details['expense_name'].append(self.expense_name)
        self.expense_details['expense_type'].append(self.expense_type)
        self.expense_details['expense_amount'].append(self.expense_amount)
        self.expense_details['expense_time'].append(self.expense_date)
        self.df = pd.DataFrame(self.expense_details, columns=list(self.expense_details.keys()))
        if os.path.exists(self.file_name):
            file_exists = True
        else:
            with(open(self.file_name, 'w') as file):
                file.write(','.join(list(self.expense_details.keys()))+'\n')
                file_exists = True

        self.df.to_csv(self.file_name,
                       index=False, mode='a', header=not file_exists)
        # mode='a' appends the data.If mode='a' is not mentioned, then it will write the file i.e delete everything and then move data to the file

class ShowingDetails:
    def __init__(self):
        self.filename = 'expense_records.csv'

    def show_expense(self):
        details = pd.read_csv(self.filename).to_dict()
        return details