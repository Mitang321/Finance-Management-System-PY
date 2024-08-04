import csv
from datetime import datetime
import matplotlib.pyplot as plt
import getpass
from fpdf import FPDF


class FinanceTracker:
    def __init__(self, filename='finance.csv'):
        self.filename = filename
        self.fields = ['date', 'type', 'amount', 'category', 'description']
        self.users_file = 'users.csv'

        # Create the files with headers if they don't exist
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            if file.tell() == 0:
                writer.writeheader()

        with open(self.users_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['username', 'password'])
            if file.tell() == 0:
                writer.writeheader()

    def add_entry(self, date, entry_type, amount, category, description):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow({'date': date, 'type': entry_type, 'amount': amount,
                            'category': category, 'description': description})

    def view_entries(self):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(
                    f"{row['date']}: {row['type']} - {row['amount']} - {row['category']} ({row['description']})")

    def delete_entry(self, date, entry_type, amount, category, description):
        entries = []
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not (row['date'] == date and row['type'] == entry_type and row['amount'] == amount and row['category'] == category and row['description'] == description):
                    entries.append(row)

        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(entries)

    def generate_monthly_report(self, month, year):
        total_expenses = 0
        total_incomes = 0

        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entry_date = datetime.strptime(row['date'], '%Y-%m-%d')
                if entry_date.month == month and entry_date.year == year:
                    if row['type'] == 'Expense':
                        total_expenses += float(row['amount'])
                    elif row['type'] == 'Income':
                        total_incomes += float(row['amount'])

        balance = total_incomes - total_expenses
        print(f"Monthly Report for {month}/{year}")
        print(f"Total Expenses: {total_expenses}")
        print(f"Total Incomes: {total_incomes}")
        print(f"Balance: {balance}")

    def generate_category_report(self, category):
        total_expenses = 0

        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['category'] == category and row['type'] == 'Expense':
                    total_expenses += float(row['amount'])

        print(f"Category Report for {category}")
        print(f"Total Expenses: {total_expenses}")

    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def is_valid_amount(self, amount_str):
        try:
            amount = float(amount_str)
            return amount > 0
        except ValueError:
            return False

    def plot_expenses_vs_income(self):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        expenses = [0] * 12
        incomes = [0] * 12

        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entry_date = datetime.strptime(row['date'], '%Y-%m-%d')
                if row['type'] == 'Expense':
                    expenses[entry_date.month - 1] += float(row['amount'])
                elif row['type'] == 'Income':
                    incomes[entry_date.month - 1] += float(row['amount'])

        plt.plot(months, expenses, label='Expenses')
        plt.plot(months, incomes, label='Incomes')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.title('Monthly Expenses vs Incomes')
        plt.legend()
        plt.show()

    def register_user(self, username, password):
        with open(self.users_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['username', 'password'])
            writer.writerow({'username': username, 'password': password})

    def authenticate_user(self, username, password):
        with open(self.users_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    return True
        return False

    def generate_expense_category_report(self):
        categories = {}
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['type'] == 'Expense':
                    if row['category'] not in categories:
                        categories[row['category']] = 0
                    categories[row['category']] += float(row['amount'])

        print("Expense Category Report")
        for category, total in categories.items():
            print(f"{category}: {total}")

    def generate_income_category_report(self):
        categories = {}
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['type'] == 'Income':
                    if row['category'] not in categories:
                        categories[row['category']] = 0
                    categories[row['category']] += float(row['amount'])

        print("Income Category Report")
        for category, total in categories.items():
            print(f"{category}: {total}")

    def export_to_pdf(self, month, year):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(
            200, 10, txt=f"Monthly Report for {month}/{year}", ln=True, align='C')

        total_expenses = 0
        total_incomes = 0

        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entry_date = datetime.strptime(row['date'], '%Y-%m-%d')
                if entry_date.month == month and entry_date.year == year:
                    pdf.cell(
                        200, 10, txt=f"{row['date']}: {row['type']} - {row['amount']} - {row['category']} ({row['description']})", ln=True)
                    if row['type'] == 'Expense':
                        total_expenses += float(row['amount'])
                    elif row['type'] == 'Income':
                        total_incomes += float(row['amount'])

        balance = total_incomes - total_expenses
        pdf.cell(200, 10, txt=f"Total Expenses: {total_expenses}", ln=True)
        pdf.cell(200, 10, txt=f"Total Incomes: {total_incomes}", ln=True)
        pdf.cell(200, 10, txt=f"Balance: {balance}", ln=True)

        pdf.output(f"Monthly_Report_{month}_{year}.pdf")


if __name__ == "__main__":
    tracker = FinanceTracker()

    while True:
        print("\nFinance Tracker")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            tracker.register_user(username, password)
            print("User registered successfully.")
        elif choice == '2':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            if tracker.authenticate_user(username, password):
                print("Login successful.")
                while True:
                    print("\nFinance Tracker")
                    print("1. Add Expense")
                    print("2. Add Income")
                    print("3. View Entries")
                    print("4. Delete Entry")
                    print("5. Generate Monthly Report")
                    print("6. Generate Category Report")
                    print("7. Plot Expenses vs Income")
                    print("8. Generate Expense Category Report")
                    print("9. Generate Income Category Report")
                    print("10. Export Monthly Report to PDF")
                    print("11. Logout")
                    user_choice = input("Choose an option: ")

                    if user_choice == '1':
                        date = input("Enter date (YYYY-MM-DD): ")
                        if not tracker.is_valid_date(date):
                            print(
                                "Invalid date format. Please enter date in YYYY-MM-DD format.")
                            continue
                        amount = input("Enter amount: ")
                        if not tracker.is_valid_amount(amount):
                            print("Invalid amount. Please enter a positive number.")
                            continue
                        amount = float(amount)
                        category = input("Enter category: ")
                        description = input("Enter description: ")
                        tracker.add_entry(
                            date, 'Expense', amount, category, description)
                    elif user_choice == '2':
                        date = input("Enter date (YYYY-MM-DD): ")
                        if not tracker.is_valid_date(date):
                            print(
                                "Invalid date format. Please enter date in YYYY-MM-DD format.")
                            continue
                        amount = input("Enter amount: ")
                        if not tracker.is_valid_amount(amount):
                            print("Invalid amount. Please enter a positive number.")
                            continue
                        amount = float(amount)
                        category = input("Enter category: ")
                        description = input("Enter description: ")
                        tracker.add_entry(
                            date, 'Income', amount, category, description)
                    elif user_choice == '3':
                        tracker.view_entries()
                    elif user_choice == '4':
                        date = input("Enter date (YYYY-MM-DD): ")
                        if not tracker.is_valid_date(date):
                            print(
                                "Invalid date format. Please enter date in YYYY-MM-DD format.")
                            continue
                        entry_type = input("Enter type (Expense/Income): ")
                        amount = input("Enter amount: ")
                        if not tracker.is_valid_amount(amount):
                            print("Invalid amount. Please enter a positive number.")
                            continue
                        category = input("Enter category: ")
                        description = input("Enter description: ")
                        tracker.delete_entry(
                            date, entry_type, amount, category, description)
                    elif user_choice == '5':
                        month = int(input("Enter month (MM): "))
                        year = int(input("Enter year (YYYY): "))
                        tracker.generate_monthly_report(month, year)
                    elif user_choice == '6':
                        category = input("Enter category: ")
                        tracker.generate_category_report(category)
                    elif user_choice == '7':
                        tracker.plot_expenses_vs_income()
                    elif user_choice == '8':
                        tracker.generate_expense_category_report()
                    elif user_choice == '9':
                        tracker.generate_income_category_report()
                    elif user_choice == '10':
                        month = int(input("Enter month (MM): "))
                        year = int(input("Enter year (YYYY): "))
                        tracker.export_to_pdf(month, year)
                    elif user_choice == '11':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Authentication failed. Please try again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
