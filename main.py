import csv
from datetime import datetime


class FinanceTracker:
    def __init__(self, filename='finance.csv'):
        self.filename = filename
        self.fields = ['date', 'type', 'amount', 'category', 'description']

        with open(self.filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            if file.tell() == 0:
                writer.writeheader()

    def add_entry(self, date, entry_type, amount, category, description):
        try:
            datetime.strptime(date, '%Y-%m-%d')  # Validate date format
        except ValueError:
            print("Invalid date format. Please enter date as YYYY-MM-DD.")
            return

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
                try:
                    entry_date = datetime.strptime(row['date'], '%Y-%m-%d')
                    if entry_date.month == month and entry_date.year == year:
                        if row['type'] == 'Expense':
                            total_expenses += float(row['amount'])
                        elif row['type'] == 'Income':
                            total_incomes += float(row['amount'])
                except ValueError:
                    print(f"Skipping invalid date format: {row['date']}")

        balance = total_incomes - total_expenses
        print(f"Monthly Report for {month}/{year}")
        print(f"Total Expenses: {total_expenses}")
        print(f"Total Incomes: {total_incomes}")
        print(f"Balance: {balance}")


if __name__ == "__main__":
    tracker = FinanceTracker()

    while True:
        print("\nFinance Tracker")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. View Entries")
        print("4. Delete Entry")
        print("5. Generate Monthly Report")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_entry(date, 'Expense', amount, category, description)
        elif choice == '2':
            date = input("Enter date (YYYY-MM-DD): ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_entry(date, 'Income', amount, category, description)
        elif choice == '3':
            tracker.view_entries()
        elif choice == '4':
            date = input("Enter date (YYYY-MM-DD): ")
            entry_type = input("Enter type (Expense/Income): ")
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.delete_entry(date, entry_type, amount,
                                 category, description)
        elif choice == '5':
            month = int(input("Enter month (MM): "))
            year = int(input("Enter year (YYYY): "))
            tracker.generate_monthly_report(month, year)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
