import csv
from datetime import datetime


class ExpenseTracker:
    def __init__(self, filename='expenses.csv'):
        self.filename = filename
        self.fields = ['date', 'amount', 'category', 'description']

        with open(self.filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            if file.tell() == 0:
                writer.writeheader()

    def add_expense(self, date, amount, category, description):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow({'date': date, 'amount': amount,
                            'category': category, 'description': description})

    def view_expenses(self):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(
                    f"{row['date']}: {row['amount']} - {row['category']} ({row['description']})")


if __name__ == "__main__":
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_expense(date, amount, category, description)
        elif choice == '2':
            tracker.view_expenses()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
