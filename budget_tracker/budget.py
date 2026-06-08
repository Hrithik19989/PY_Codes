import pandas as pd
from datetime import datetime
from pathlib import Path

FILE = Path("budget.csv")
COLUMNS = ["date", "type", "category", "amount", "description"]

def load_data():
    if not FILE.exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(FILE, parse_dates=["date"])

def save_data(df):
    df.to_csv(FILE, index=False)
    
CATEGORIES = {
    "income":  ["salary", "freelance", "business", "investment", "other"],
    "expense": ["food", "transport", "rent", "utilities", "health",
                "entertainment", "shopping", "education", "other"]
}

def add_transaction(trans_type, category, amount, description):
    df = load_data()

    new_row = pd.DataFrame([{
        "date":        datetime.now().strftime("%Y-%m-%d"),
        "type":        trans_type,
        "category":    category,
        "amount":      round(amount, 2),
        "description": description
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    print(f"  ✓ Added: {trans_type} | {category} | ₹{amount:.2f} | {description}")
    
def view_transactions(month=None):
    df = load_data()

    if df.empty:
        print("  No transactions yet.")
        return

    if month:
        df = df[df["date"].dt.month == month]
        if df.empty:
            print(f"  No transactions for month {month}.")
            return

    print(f"\n  {'DATE':<12} {'TYPE':<10} {'CATEGORY':<15} {'AMOUNT':>10} {'DESCRIPTION'}")
    print("  " + "-" * 65)

    for _, row in df.iterrows():
        amount_str = f"₹{row['amount']:,.2f}"
        print(f"  {str(row['date'])[:10]:<12} {row['type']:<10} {row['category']:<15} {amount_str:>10} {row['description']}")
    print()
    
def monthly_summary():
    df = load_data()

    if df.empty:
        print("  No transactions yet.")
        return

    df["month"] = df["date"].dt.to_period("M")
    grouped = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)

    print(f"\n  {'MONTH':<12} {'INCOME':>12} {'EXPENSES':>12} {'BALANCE':>12}")
    print("  " + "-" * 50)

    for month, row in grouped.iterrows():
        income   = row.get("income", 0)
        expense  = row.get("expense", 0)
        balance  = income - expense
        sign     = "+" if balance >= 0 else ""
        print(f"  {str(month):<12} ₹{income:>10,.2f} ₹{expense:>10,.2f} {sign}₹{balance:>9,.2f}")
    print()
    
def category_breakdown(month=None):
    df = load_data()

    if df.empty:
        print("  No transactions yet.")
        return

    if month:
        df = df[df["date"].dt.month == month]

    expenses = df[df["type"] == "expense"]

    if expenses.empty:
        print("  No expenses found.")
        return

    breakdown = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)
    total     = breakdown.sum()

    print(f"\n  {'CATEGORY':<20} {'AMOUNT':>10} {'%':>8}")
    print("  " + "-" * 42)

    for cat, amount in breakdown.items():
        pct = (amount / total) * 100
        bar = "█" * int(pct / 5)
        print(f"  {cat:<20} ₹{amount:>8,.2f} {pct:>6.1f}% {bar}")

    print(f"\n  {'TOTAL':<20} ₹{total:>8,.2f}")
    print()
    
def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  Amount must be greater than 0.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid number.")

def get_choice(prompt, options):
    print(f"\n  Options: {', '.join(f'{i+1}.{o}' for i, o in enumerate(options))}")
    while True:
        try:
            choice = int(input(f"  {prompt}: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"  Enter a number between 1 and {len(options)}.")
        except ValueError:
            print("  Please enter a valid number.")

def get_month():
    while True:
        try:
            month = int(input("  Enter month number (1-12, 0 for all): "))
            if 0 <= month <= 12:
                return month if month != 0 else None
            print("  Enter a number between 0 and 12.")
        except ValueError:
            print("  Please enter a valid number.")
            
def menu():
    print("\n  💰 BUDGET TRACKER")
    print("  " + "=" * 25)
    print("  1. Add income")
    print("  2. Add expense")
    print("  3. View transactions")
    print("  4. Monthly summary")
    print("  5. Category breakdown")
    print("  6. Exit")

def main():
    while True:
        menu()
        choice = input("\n  Choose (1-6): ").strip()

        if choice in ("1", "2"):
            trans_type = "income" if choice == "1" else "expense"
            category   = get_choice("Choose category", CATEGORIES[trans_type])
            amount     = get_float("  Amount: ₹")
            description = input("  Description: ").strip()
            add_transaction(trans_type, category, amount, description)

        elif choice == "3":
            month = get_month()
            view_transactions(month)

        elif choice == "4":
            monthly_summary()

        elif choice == "5":
            month = get_month()
            category_breakdown(month)

        elif choice == "6":
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("  Invalid choice. Enter 1 to 6.")

if __name__ == "__main__":
    main()