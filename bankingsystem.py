"""
Banking System - Python Mini Project
------------------------------------
Concepts used: variables & data types, conditionals, loops, functions,
lists & dictionaries, string operations, and modules (random, datetime).

Data is stored in memory (a dictionary), so it resets when the program ends.
"""

import random
from datetime import datetime

# ------------------------------------------------------------------
# Data storage
# accounts = {
#     "1234567890": {
#         "name": "Riya Sharma",
#         "phone": "9876543210",
#         "pin": "1234",
#         "balance": 0.0,
#         "transactions": [ "2026-09-21 10:30:00 | Deposit | +500.00 | Balance: 500.00" ]
#     }
# }
# ------------------------------------------------------------------
accounts = {}


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def now():
    """Return the current date and time as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_account_number():
    """Generate a unique 10-digit account number using the random module."""
    while True:
        number = str(random.randint(1000000000, 9999999999))
        if number not in accounts:
            return number


def get_amount(prompt):
    """Ask for an amount and return it as a positive float (or None if invalid)."""
    try:
        amount = float(input(prompt).strip())
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None
    if amount <= 0:
        print("Amount must be greater than zero.")
        return None
    return amount


def add_transaction(acc_no, kind, amount, note=""):
    """Record a transaction (with date & time) in the account's history."""
    account = accounts[acc_no]
    sign = "+" if kind in ("Deposit", "Transfer In") else "-"
    entry = f"{now()} | {kind:<12} | {sign}{amount:.2f} | Balance: {account['balance']:.2f}"
    if note:
        entry += f" | {note}"
    account["transactions"].append(entry)


def mask(acc_no):
    """Hide all but the last 4 digits of an account number."""
    return "******" + acc_no[-4:]


# ------------------------------------------------------------------
# Main menu features
# ------------------------------------------------------------------
def create_account():
    print("\n--- CREATE ACCOUNT ---")

    name = input("Enter your name: ").strip().title()
    if name == "" or not name.replace(" ", "").isalpha():
        print("Invalid name. Use letters and spaces only.")
        return

    phone = input("Enter phone number (10 digits): ").strip()
    if not (phone.isdigit() and len(phone) == 10):
        print("Invalid phone number. It must contain exactly 10 digits.")
        return

    pin = input("Create a 4-digit PIN: ").strip()
    if not (pin.isdigit() and len(pin) == 4):
        print("Invalid PIN. It must be exactly 4 digits.")
        return

    confirm = input("Confirm PIN: ").strip()
    if pin != confirm:
        print("PINs do not match. Account not created.")
        return

    acc_no = generate_account_number()
    accounts[acc_no] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": [],
    }

    print("\nAccount created successfully!")
    print(f"Name           : {name}")
    print(f"Account Number : {acc_no}   (please remember this)")


def login():
    """Return the account number if login succeeds, otherwise None."""
    print("\n--- LOGIN ---")
    acc_no = input("Enter account number: ").strip()

    if acc_no not in accounts:
        print("Account not found.")
        return None

    attempts = 3
    while attempts > 0:
        pin = input("Enter PIN: ").strip()
        if pin == accounts[acc_no]["pin"]:
            print(f"\nWelcome, {accounts[acc_no]['name']}!")
            return acc_no
        attempts -= 1
        if attempts > 0:
            print(f"Incorrect PIN. {attempts} attempt(s) left.")

    print("Too many wrong attempts. Returning to main menu.")
    return None


# ------------------------------------------------------------------
# Account menu features (after login)
# ------------------------------------------------------------------
def check_balance(acc_no):
    print(f"\nCurrent balance: Rs. {accounts[acc_no]['balance']:.2f}")


def deposit(acc_no):
    print("\n--- DEPOSIT ---")
    amount = get_amount("Enter amount to deposit: ")
    if amount is None:
        return

    accounts[acc_no]["balance"] += amount
    add_transaction(acc_no, "Deposit", amount)
    print(f"Rs. {amount:.2f} deposited successfully.")
    check_balance(acc_no)


def withdraw(acc_no):
    print("\n--- WITHDRAW ---")
    amount = get_amount("Enter amount to withdraw: ")
    if amount is None:
        return

    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance.")
        return

    accounts[acc_no]["balance"] -= amount
    add_transaction(acc_no, "Withdrawal", amount)
    print(f"Rs. {amount:.2f} withdrawn successfully.")
    check_balance(acc_no)


def transfer(acc_no):
    print("\n--- TRANSFER MONEY ---")
    receiver = input("Enter receiver account number: ").strip()

    if receiver == acc_no:
        print("You cannot transfer money to your own account.")
        return
    if receiver not in accounts:
        print("Receiver account not found.")
        return

    print(f"Receiver: {accounts[receiver]['name']} ({mask(receiver)})")
    amount = get_amount("Enter amount to transfer: ")
    if amount is None:
        return

    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance.")
        return

    pin = input("Enter your PIN to confirm: ").strip()
    if pin != accounts[acc_no]["pin"]:
        print("Incorrect PIN. Transfer cancelled.")
        return

    # Move the money
    accounts[acc_no]["balance"] -= amount
    accounts[receiver]["balance"] += amount

    # Record it in both accounts
    add_transaction(acc_no, "Transfer Out", amount, f"To {mask(receiver)}")
    add_transaction(receiver, "Transfer In", amount, f"From {mask(acc_no)}")

    print(f"Rs. {amount:.2f} transferred to {accounts[receiver]['name']} successfully.")
    check_balance(acc_no)


def view_history(acc_no):
    print("\n--- TRANSACTION HISTORY ---")
    history = accounts[acc_no]["transactions"]

    if len(history) == 0:
        print("No transactions yet.")
        return

    for number, entry in enumerate(history, start=1):
        print(f"{number}. {entry}")


def change_pin(acc_no):
    print("\n--- CHANGE PIN ---")
    old_pin = input("Enter old PIN: ").strip()
    if old_pin != accounts[acc_no]["pin"]:
        print("Incorrect old PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("Invalid PIN. It must be exactly 4 digits.")
        return
    if new_pin == old_pin:
        print("New PIN must be different from the old PIN.")
        return

    confirm = input("Confirm new PIN: ").strip()
    if new_pin != confirm:
        print("PINs do not match. PIN not changed.")
        return

    accounts[acc_no]["pin"] = new_pin
    print("PIN changed successfully.")


# ------------------------------------------------------------------
# Menus
# ------------------------------------------------------------------
def account_menu(acc_no):
    """Menu shown after a successful login. Runs until the user logs out."""
    while True:
        print("\n" + "=" * 32)
        print("         ACCOUNT MENU")
        print("=" * 32)
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            check_balance(acc_no)
        elif choice == "2":
            deposit(acc_no)
        elif choice == "3":
            withdraw(acc_no)
        elif choice == "4":
            transfer(acc_no)
        elif choice == "5":
            view_history(acc_no)
        elif choice == "6":
            change_pin(acc_no)
        elif choice == "7":
            print("\nLogged out successfully. Returning to main menu...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


def main_menu():
    while True:
        print("\n" + "=" * 32)
        print("        BANKING SYSTEM")
        print("=" * 32)
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            acc_no = login()
            if acc_no is not None:
                account_menu(acc_no)
        elif choice == "3":
            print("\nThank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


# ------------------------------------------------------------------
# Program starts here
# ------------------------------------------------------------------
if __name__ == "__main__":
    main_menu()