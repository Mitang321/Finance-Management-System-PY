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


if __name__ == "__main__":
    tracker = FinanceTracker()

    while True:
        print("\nFinance Tracker")
        print("1. Add Expense")
        print("2. Add Income")
        print("3. View Entries")
        print("4. Exit")
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
            break
        else:
            print("Invalid choice. Please try again.")
