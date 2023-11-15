# -*- coding: utf-8 -*-
import sqlite3
import bcrypt
import random
import string
import math
import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


# Welcome text
WELCOME_TEXT = """                         
                                                                              ,---------------------------,                                                         
                                                                              |  /---------------------\  |
                                                                              | |                       | |
                                                                              | |     we value          | |
                                                                              | |      customer         | |
                                                                              | |       time & needs    | |
                                                                              | |                       | |
                                                                              |  \_____________________/  |
                                                                              |___________________________|
                                                                            ,---\_____     []     _______/------,
                                                                          /         /______________\           /|                                                                           
                                                                        /___________________________________ /  | ___
                                                                        |                                   |   |    )
                                                                        |  _ _ _                 [-------]  |   |   (
                                                                        |  o o o                 [-------]  |  /    _)_
                                                                        |__________________________________ |/     /  /
                                                                    /-------------------------------------/|      ( )/
                                                                  /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
                                                                /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
                                                                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


888       888 8888888888 888       .d8888b.   .d88888b.  888b     d888 8888888888       88888888888  .d88888b.        888       .d88888b.   .d8888b.         d8888 888            888888b.          d8888 888b    888 888    d8P  
888   o   888 888        888      d88P  Y88b d88P" "Y88b 8888b   d8888 888                  888     d88P" "Y88b       888      d88P" "Y88b d88P  Y88b       d88888 888            888  "88b        d88888 8888b   888 888   d8P   
888  d8b  888 888        888      888    888 888     888 88888b.d88888 888                  888     888     888       888      888     888 888    888      d88P888 888            888  .88P       d88P888 88888b  888 888  d8P    
888 d888b 888 8888888    888      888        888     888 888Y88888P888 8888888              888     888     888       888      888     888 888            d88P 888 888            8888888K.      d88P 888 888Y88b 888 888d88K     
888d88888b888 888        888      888        888     888 888 Y888P 888 888                  888     888     888       888      888     888 888           d88P  888 888            888  "Y88b    d88P  888 888 Y88b888 8888888b    
88888P Y88888 888        888      888    888 888     888 888  Y8P  888 888                  888     888     888       888      888     888 888    888   d88P   888 888            888    888   d88P   888 888  Y88888 888  Y88b   
8888P   Y8888 888        888      Y88b  d88P Y88b. .d88P 888   "   888 888                  888     Y88b. .d88P       888      Y88b. .d88P Y88b  d88P  d8888888888 888            888   d88P  d8888888888 888   Y8888 888   Y88b  
888P     Y888 8888888888 88888888  "Y8888P"   "Y88888P"  888       888 8888888888           888      "Y88888P"        88888888  "Y88888P"   "Y8888P"  d88P     888 88888888       8888888P"  d88P     888 888    Y888 888    Y88b 



                    888888888         .d8888b.                           88888888888                                 d8888                          8888888b.                            .d8888b.                                   
                    888              d88P  Y88b       o                      888           o                        d88888       o                  888   Y88b       o                  d88P  Y88b       o                          
                    888              Y88b.           d8b                     888          d8b                      d88P888      d8b                 888    888      d8b                 Y88b.           d8b                         
                    8888888b.         "Y888b.       d888b                    888         d888b                    d88P 888     d888b                888   d88P     d888b                 "Y888b.       d888b                        
                         "Y88b           "Y88b. "Y888888888P"                888     "Y888888888P"               d88P  888 "Y888888888P"            8888888P"  "Y888888888P"                "Y88b. "Y888888888P"                    
                           888             "888   "Y88888P"                  888       "Y88888P"                d88P   888   "Y88888P"              888 T88b     "Y88888P"                    "888   "Y88888P"                      
                    Y88b  d88P       Y88b  d88P   d88P"Y88b                  888       d88P"Y88b               d8888888888   d88P"Y88b              888  T88b    d88P"Y88b              Y88b  d88P   d88P"Y88b                      
                     "Y8888P"         "Y8888P"   dP"     "Yb                 888      dP"     "Yb             d88P     888  dP"     "Yb             888   T88b  dP"     "Yb              "Y8888P"   dP"     "Yb          
  """
# Closing text
CLOSE_TEXT = """

 ████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗    ██╗   ██╗ ██████╗ ██╗   ██╗    ███████╗ ██████╗ ██████╗     ██╗   ██╗███████╗██╗███╗   ██╗ ██████╗      ██████╗ ██╗   ██╗██████╗     ██████╗  █████╗ ███╗   ██╗██╗  ██╗ █████╗ ██████╗ ██████╗      ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗██╗
  ╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██╔════╝██╔═══██╗██╔══██╗    ██║   ██║██╔════╝██║████╗  ██║██╔════╝     ██╔═══██╗██║   ██║██╔══██╗    ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔══██╗██╔══██╗██╔══██╗    ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██║
     ██║   ███████║███████║██╔██╗ ██║█████╔╝      ╚████╔╝ ██║   ██║██║   ██║    █████╗  ██║   ██║██████╔╝    ██║   ██║███████╗██║██╔██╗ ██║██║  ███╗    ██║   ██║██║   ██║██████╔╝    ██████╔╝███████║██╔██╗ ██║█████╔╝ ███████║██████╔╝██████╔╝    ██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗  ██║
     ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗       ╚██╔╝  ██║   ██║██║   ██║    ██╔══╝  ██║   ██║██╔══██╗    ██║   ██║╚════██║██║██║╚██╗██║██║   ██║    ██║   ██║██║   ██║██╔══██╗    ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██╔══██║██╔═══╝ ██╔═══╝     ██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝  ╚═╝
     ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝    ██║     ╚██████╔╝██║  ██║    ╚██████╔╝███████║██║██║ ╚████║╚██████╔╝    ╚██████╔╝╚██████╔╝██║  ██║    ██████╔╝██║  ██║██║ ╚████║██║  ██╗██║  ██║██║     ██║██╗      ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗██╗
     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝       ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝

"""
class BankDatabase:
    def __init__(self, db_name="bankapp.db"):
        try:
            self.conn = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
            self.conn.row_factory = sqlite3.Row  # Set row_factory for named columns
            self.cursor = self.conn.cursor()
            self.create_tables()
            self.create_admin(
                self.cursor, self.conn
            )  # Create admin user on initialization
        except sqlite3.Error as e:
            print("Database connection error:", e)

    def create_tables(self):
        # Create necessary tables if they don't exist
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, 
                              balance REAL, account_number TEXT UNIQUE)"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS transactions
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, transaction_type TEXT, 
                              amount REAL, transaction_time DATETIME)"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS admins
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)"""
        )
        self.conn.commit()

    def close_connection(self):
        # Close the database connection
        self.conn.close()

    # Function to fetch user transactions from the database
    def fetch_user_transactions(self, username):
        # Execute a database query to fetch transactions for the given username
        self.cursor.execute("SELECT * FROM transactions WHERE username=?", (username,))
        transactions = self.cursor.fetchall()

        # Prepare a list of dictionaries containing transaction data
        transaction_list = []
        for transaction in transactions:
            transaction_data = {
                "transaction_type": transaction["transaction_type"],
                "amount": transaction["amount"],
                "transaction_time": transaction["transaction_time"],
            }
            transaction_list.append(transaction_data)

        # Return the list of user transactions
        return transaction_list

    # Function to get float input from user
    def get_float_input(self, prompt):
        while True:
            try:
                # Ask the user for input using the provided prompt
                user_input = input(prompt).replace(" ", "")

                # Convert the user input to a float
                amount = float(user_input)

                # Check if the input is non-negative
                if amount >= 0:
                    return amount
                else:
                    print("Invalid input. Please enter a non-negative value.")
            except ValueError:
                # Handle the case where the user enters invalid input (not a number)
                print("Invalid input. Please enter a valid numeric value.")

# Function to generate a random account number
    def generate_random_account_number(self):
        account_number = "".join(random.choices(string.digits, k=10))
        return account_number

    # Function to validate the password
    def is_valid_password(self, password):
        # Check if the password meets certain criteria (e.g., length, uppercase, lowercase, digits, special characters)
        # Return True if the password is valid, otherwise return False

        # Check if the password has at least 8 characters
        if len(password) < 8:
            return False

        # Check if the password contains at least one uppercase letter
        if not any(char.isupper() for char in password):
            return False

        # Check if the password contains at least one lowercase letter
        if not any(char.islower() for char in password):
            return False

        # Check if the password contains at least one digit
        if not any(char.isdigit() for char in password):
            return False

        # Check if the password contains at least one special character (e.g., !@#$%^&*)
        special_characters = r"[!@#$%^&*]"
        if not re.search(special_characters, password):
            return False

        return True

    # Function to handle user deposit
    def user_deposit(self, user, amount):
        if amount >= 10 and amount % 10 == 0:
            # Calculate the new balance after deposit
            user_balance = user["balance"] + amount

            # Update user's balance in the database
            self.cursor.execute(
                "UPDATE users SET balance=? WHERE account_number=?",
                (user_balance, user["account_number"]),
            )

            # Get the current timestamp for the transaction
            transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insert the deposit transaction into the transactions table
            self.cursor.execute(
                "INSERT INTO transactions (username, transaction_type, amount, transaction_time) VALUES (?, ?, ?, ?)",
                (user["username"], "Deposit", amount, transaction_time),
            )
            self.conn.commit()

            # Log the deposit transaction
            self.log_transaction(user["username"], "Deposit", amount, user_balance)

            # Fetch the updated balance from the database
            self.cursor.execute(
                "SELECT balance FROM users WHERE account_number=?",
                (user["account_number"],),
            )
            updated_balance = self.cursor.fetchone()[0]

            # Print deposited amount and updated balance
            print(f"Deposited: R{amount}")
            print(f"Current Balance: R{updated_balance}")  # Display updated balance after deposit
            return amount
        else:
            # Print error message for invalid deposit amount
            print(
                "Invalid deposit amount. Please enter an amount above or equal to 10 and in multiples of 10."
            )
            return None
    # Function to handle user withdrawal
    def user_withdraw(self, user, amount):
        if amount >= 60 and amount % 10 == 0:
            try:
                # Fetch the user's current balance from the database
                self.cursor.execute(
                    "SELECT balance FROM users WHERE username=?", (user["username"],)
                )
                user_balance = self.cursor.fetchone()[0]

                # Check if the user has sufficient balance for the withdrawal
                if user_balance >= amount:
                    # Calculate the new balance after withdrawal
                    new_balance = user_balance - amount

                    # Update user's balance in the database
                    self.cursor.execute(
                        "UPDATE users SET balance=? WHERE username=?",
                        (new_balance, user["username"]),
                    )

                    # Get the current timestamp for the transaction
                    transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Insert the withdrawal transaction into the transactions table
                    self.cursor.execute(
                        "INSERT INTO transactions (username, transaction_type, amount, transaction_time) VALUES (?, ?, ?, ?)",
                        (user["username"], "Withdrawal", amount, transaction_time),
                    )
                    self.conn.commit()

                    # Log the withdrawal transaction
                    self.log_transaction(
                        user["username"], "Withdrawal", amount, new_balance
                    )

                    # Fetch the updated balance from the database
                    self.cursor.execute(
                        "SELECT balance FROM users WHERE username=?",
                        (user["username"],),
                    )
                    updated_balance = self.cursor.fetchone()[0]

                    # Print withdrawn amount and updated balance
                    print(f"Withdrawn: R{amount}")
                    print(f"Current Balance: R{updated_balance}")  # Display updated balance after withdrawal
                    return amount
                else:
                    # Print error message for insufficient balance
                    return "Insufficient balance for withdrawal."
            except sqlite3.Error as e:
                # Handle database error and print error message
                print("Database error:", e)
                return "An error occurred while processing the withdrawal. Please try again later."
        else:
            # Print error message for invalid withdrawal amount
            print(
                "Invalid withdrawal amount. Please enter an amount above 50 and in multiples of 10."
            )
            return None

    # Function to log transactions in transaction_log.txt file
    def log_transaction(
        self, username, transaction_type, amount, transaction_time, balance
    ):
        with open("transaction_log.txt", "a") as file:
            log_entry = f"Username: {username}, Transaction Type: {transaction_type}, Amount: {amount}, Balance: {balance}, Time: {transaction_time}\n"
            file.write(log_entry)
        print("Transaction logged successfully.")

    # Function to validate initial deposit amount input
    def validate_initial_deposit(self, input_value):
        try:
            deposit_amount = float(input_value)
            if deposit_amount < 0:
                print("Initial deposit amount cannot be negative. Please enter a valid amount.")
                return None
            return deposit_amount
        except ValueError:
            print("Invalid input. Please enter a valid numeric value for the deposit amount.")
            return None

    # Function to generate a random password
    def generate_random_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    # Function to create a new user account
    def create_account(self):
        while True:
            username = input("Enter your username: ")

            # Validate username (no spaces and unique)
            if " " in username:
                print("Username cannot contain spaces. Please choose a different username.")
                continue

            self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                print("Username already in use. Please choose a different username.")
            else:
                break

        while True:
            # Generate a random password
            generated_password = self.generate_random_password()
            print(f"Generated Password: {generated_password}")

            # Ask the user if they want to use the generated password
            use_generated_password = input("Do you want to use the generated password? (yes/no): ").lower()

            if use_generated_password == "yes":
                password = generated_password
                break
            elif use_generated_password == "no":
                # Ask the user to enter a password
                password = input("Enter your password (at least 8 characters with special characters): ")

                # Validate password
                if not self.is_valid_password(password):
                    print(
                        "Invalid password. Please ensure your password has at least 8 characters with uppercase letters, lowercase letters, digits, and special characters.")
                    continue
                break
            else:
                print("Invalid choice! Please enter 'yes' or 'no'.")

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        while True:
            initial_deposit_input = input("Enter initial deposit amount: R")
            initial_deposit = self.validate_initial_deposit(initial_deposit_input)
            if initial_deposit is not None:
                break

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        account_number = self.generate_random_account_number()

        # Store user data in the users table
        self.cursor.execute(
            "INSERT INTO users (username, password, balance, account_number) VALUES (?, ?, ?, ?)",
            (username, hashed_password, initial_deposit, account_number),
        )

        # Store user data in bankdata.txt
        with open("bankdata.txt", "a") as bankdata_file:
            bankdata_file.write(
                f"Username: {username}, Account Number: {account_number}\n"
            )

        # Log initial deposit transaction in the transactions table
        self.cursor.execute(
            "INSERT INTO transactions (username, transaction_type, amount, transaction_time) VALUES (?, ?, ?, ?)",
            (
                username,
                "Initial Deposit",
                initial_deposit,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        self.conn.commit()
        # Print the generated account number and prompt the user to store it securely
        print(f"Account created successfully! Your account number is: {account_number}")
        print("Please make sure to store your account number and password securely.")

    # Function to handle user actions
    def handle_user_actions(self, user_data):
        calculator = Calculator()  # Create an instance of the Calculator class
        print(f"Welcome, {user_data['username']}!")
        while True:
            # Display menu options to the user
            print("\n1. Deposit")
            print("2. Withdraw")
            print("3. View Balance")
            print("4. View Transaction History")
            print("5. Financial Calculator")
            print("6. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                # Handle deposit functionality
                deposit_amount = float(input("Enter deposit amount: R"))
                if deposit_amount > 0:
                    deposited_amount = self.user_deposit(user_data, deposit_amount)
                    if deposited_amount is not None:
                        user_row = self.cursor.execute(
                            "SELECT * FROM users WHERE username=?",
                            (user_data["username"],),
                        ).fetchone()
                        user_data = dict(user_row)
                        print(f"Deposited: R{deposited_amount}")
                        print(f"Current Balance: R{user_data['balance']:.2f}")
                else:
                    print("Invalid deposit amount. Please enter a positive value.")

            elif choice == "2":
                # Handle withdrawal functionality
                withdrawal_amount = float(input("Enter withdrawal amount: R"))
                if withdrawal_amount > 0:
                    withdrawn_amount = self.user_withdraw(user_data, withdrawal_amount)
                    if isinstance(withdrawn_amount, float):
                        user_row = self.cursor.execute(
                            "SELECT * FROM users WHERE username=?",
                            (user_data["username"],),
                        ).fetchone()
                        user_data = dict(user_row)
                        print(f"Withdrawn: R{withdrawn_amount}")
                        print(f"Current Balance: R{user_data['balance']:.2f}")
                    else:
                        print(
                            withdrawn_amount
                        )  # Display error message if withdrawal fails
                else:
                    print("Invalid withdrawal amount. Please enter a positive value.")

            elif choice == "3":
                # Display current balance
                print(f"Current Balance: R{user_data['balance']:.2f}")

            elif choice == "4":
                # Handle viewing transaction history
                transactions = self.fetch_user_transactions(user_data["username"])
                print("\nTransaction History:")
                for transaction in transactions:
                    print(
                        f"Type: {transaction['transaction_type']}, Amount: R{transaction['amount']:.2f}, Time: {transaction['transaction_time']}"
                    )

            elif choice == "5":
                # Financial Calculator option
                calculator.financial_calculator()

            elif choice == "6":
                # Logout the user and exit the loop
                print("Logout successful.")
                break

            else:
                print("Invalid choice! Please try again.")

    # Function to handle admin actions
    def handle_admin_actions(self):
        admin_username = input("Enter admin username: ")
        admin_password = input("Enter admin password: ")

        # Authenticate admin
        self.cursor.execute("SELECT * FROM admins WHERE username=?", (admin_username,))
        admin_data = self.cursor.fetchone()

        if admin_data and bcrypt.checkpw(
                admin_password.encode("utf-8"), admin_data[2].encode("utf-8")
        ):
            print("Admin login successful!")
            while True:
                print("\n1. Remove User")
                print("2. View All Users")
                print("3. Logout")
                admin_choice = input("Enter your choice: ")

                if admin_choice == "1":
                    account_number = input("Enter account number to remove user: ")
                    self.remove_user(account_number)
                elif admin_choice == "2":
                    self.cursor.execute("SELECT * FROM users")
                    users = self.cursor.fetchall()
                    print("\nAll Users:")
                    for user in users:
                        print(
                            f"Username: {user[1]}, Account Number: {user[4]}, Balance: R{user[3]}"
                        )
                elif admin_choice == "3":
                    print("Admin logout successful.")
                    break
                else:
                    print("Invalid choice! Please try again.")
        else:
            print("Invalid admin credentials. Access denied.")

    # Function to remove user
    def remove_user(self, account_number):
        self.cursor.execute(
            "SELECT * FROM users WHERE account_number=?", (account_number,)
        )
        user_data = self.cursor.fetchone()

        if user_data:
            self.cursor.execute(
                "DELETE FROM users WHERE account_number=?", (account_number,)
            )
            self.cursor.execute(
                "DELETE FROM transactions WHERE username=?", (user_data[1],)
            )
            self.conn.commit()
            print(
                f"User with account number {account_number} has been removed successfully."
            )
        else:
            print("Invalid account number. Please try again.")

    # Function to handle user login
    def login(self):
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user_data = self.cursor.fetchone()

            if user_data and bcrypt.checkpw(
                    password.encode("utf-8"), user_data[2].encode("utf-8")
            ):
                print("Login successful!")
                return user_data
            else:
                print("Invalid username or password. Please try again.")
                continue

    # Function to create an admin user
    def create_admin(self, cursor, conn):
        cursor.execute(
            "INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)",
            (
                "admin",
                bcrypt.hashpw("admin@123".encode("utf-8"), bcrypt.gensalt()).decode(
                    "utf-8"
                ),
            ),
        )
        conn.commit()
class Calculator:
    def financial_calculator(self):
        while True:
            print("\nFinancial Calculator")
            print("1. Invest")
            print("2. Loan")
            print("3. Return to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                # Compound Interest Calculator
                principal = float(input("Enter principal amount: R"))
                rate_of_interest = float(input("Enter annual interest rate (%): "))
                time = float(input("Enter time period (in years): "))
                interest_type = input("Enter interest type (simple/compound): ")

                r = rate_of_interest / 100
                if interest_type.lower() == "simple":
                    # Simple Interest Calculation
                    simple_interest = principal * r * time
                    total_amount = principal + simple_interest
                    print(f"Simple Interest: R{simple_interest:.2f}")
                    print(f"Total return: R{total_amount:.2f}")

                elif interest_type.lower() == "compound":
                    # Compound Interest Calculation
                    compound_interest = principal * math.pow((1 + r), time) - principal
                    total_amount = principal + compound_interest
                    print(f"Compound Interest: R{compound_interest:.2f}")
                    print(f"Total return: R{total_amount:.2f}")
                else:
                    print("Invalid interest type. Please enter 'simple' or 'compound'.")
                    return

            elif choice == "2":
                # Bond Repayment Calculator
                present_value = float(input("Enter present value of the house: R"))
                annual_interest_rate = float(input("Enter annual interest rate (%): "))
                number_of_months = int(input("Enter number of months to repay the bond: "))

                i = annual_interest_rate / 100 / 12
                n = number_of_months

                monthly_repayment = (i * present_value) / (1 - math.pow((1 + i), -n))
                print(f"Monthly Repayment: R{monthly_repayment:.2f}")
            elif choice == "3":
                while True:
                    another_calculation = input("Do you want to perform another calculation? (yes/no): ").lower()
                    if another_calculation == "no":
                        return
                    elif another_calculation == "yes":
                        break
                    else:
                        print("Invalid choice! Please enter 'yes' or 'no'.")
                        # Ask again if the input is neither 'yes' nor 'no'
            else:
                print("Invalid choice! Please enter a valid option (1, 2, or 3).")

if __name__ == "__main__":
    bank_db = BankDatabase()

    while True:
        try:
            print(WELCOME_TEXT)
            print("1. Create Account")
            print("2. Login")
            print("3. Admin - Remove User")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                bank_db.create_account()
            elif choice == "2":
                user_data = bank_db.login()
                if user_data:
                    bank_db.handle_user_actions(user_data)
            elif choice == "3":
                bank_db.handle_admin_actions()
            elif choice == "4":
                print(CLOSE_TEXT)
                bank_db.close_connection()
                break
            else:
                print("Invalid choice! Please try again.")

        except Exception as e:
            print("An unexpected error occurred:", e)