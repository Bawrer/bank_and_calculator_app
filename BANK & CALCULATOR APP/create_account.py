import random
import sqlite3
import string
from tkinter import Tk, Label, Frame, Entry, Button, messagebox
import bcrypt
import os

class BankDatabase:
    def __init__(self, db_file="bankapp.db"):
        db_file = os.path.abspath(db_file)
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
        print("BankDatabase instance initialized")

    def create_tables(self):
        with self.conn:
            cursor = self.conn.cursor()

            # Create the accounts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    account_number TEXT PRIMARY KEY,
                    username TEXT,
                    salt TEXT,
                    hashed_password TEXT,
                    balance REAL
                )
            ''')

            # Create the transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number TEXT,
                    amount REAL,
                    description TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
                )
            ''')

            # Add the missing column 'account_number' to the transactions table
            cursor.execute('PRAGMA foreign_keys=off;')
            cursor.execute('BEGIN TRANSACTION;')
            cursor.execute('ALTER TABLE transactions RENAME TO _transactions_backup;')

            cursor.execute('''
                CREATE TABLE transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number TEXT,
                    amount REAL,
                    description TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
                )
            ''')

            cursor.execute('INSERT INTO transactions SELECT * FROM _transactions_backup;')
            cursor.execute('DROP TABLE _transactions_backup;')
            cursor.execute('COMMIT;')
            cursor.execute('PRAGMA foreign_keys=on;')

        print("Tables created")

    def store_initial_deposit(self, account_number, initial_deposit):
        with self.conn:
            cursor = self.conn.cursor()

            # Insert the initial deposit as a transaction
            cursor.execute('''
                INSERT INTO transactions (account_number, amount, description)
                VALUES (?, ?, ?)
            ''', (account_number, initial_deposit, 'Initial Deposit'))

    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=10))

    def generate_random_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return salt.decode('utf-8'), hashed_password.decode('utf-8')

    def is_valid_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create_account(self, username, password, confirm_password, initial_deposit):
        if not all((username, password, confirm_password, initial_deposit)):
            raise ValueError("All fields must be filled")

        if password != confirm_password:
            raise ValueError("Passwords do not match")

        salt, hashed_password = self.hash_password(password)

        account_number = self.generate_account_number()

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO accounts (account_number, username, salt, hashed_password, balance) VALUES (?, ?, ?, ?, ?)",
                           (account_number, username, salt, hashed_password, float(initial_deposit)))
            print("Account created")

        # Store the initial deposit as a transaction
        self.store_initial_deposit(account_number, float(initial_deposit))

        # Commit the changes to the database
        self.conn.commit()

class BankApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank App")
        self.bank_db = BankDatabase()
        self.setup_ui()

    def setup_ui(self):
        self.master.configure(bg="#3498DB")  # Set the background color of the main window

        label = Label(self.master, text="WELCOME TO 5 STARS LOCAL BANKAPP", font=("Helvetica", 16), bg="#3498DB", fg="white")
        label.pack(pady=20)

        frame = Frame(master=self.master, bg="#3498DB")
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        label = Label(master=frame, text='CREATE A BANK ACCOUNT', font=("Helvetica", 12), bg="#3498DB", fg="white")
        label.pack(pady=12, padx=10)

        self.user_entry = Entry(master=frame, bg="#ECF0F1", fg="#2C3E50")
        self.user_entry.insert(0, "Username")
        self.user_entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, "Username"))
        self.user_entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, "Username"))
        self.user_entry.pack(pady=12, padx=10)

        self.user_pass = Entry(master=frame, show="*", bg="#ECF0F1", fg="#2C3E50")
        self.user_pass.insert(0, "Password")
        self.user_pass.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, "Password"))
        self.user_pass.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, "Password"))
        self.user_pass.pack(pady=12, padx=10)

        self.confirm_pass = Entry(master=frame, show="*", bg="#ECF0F1", fg="#2C3E50")
        self.confirm_pass.insert(0, "Confirm Password")
        self.confirm_pass.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, "Confirm Password"))
        self.confirm_pass.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, "Confirm Password"))
        self.confirm_pass.pack(pady=12, padx=10)

        self.initial_deposit_entry = Entry(master=frame, bg="#ECF0F1", fg="#2C3E50")
        self.initial_deposit_entry.insert(0, "Initial Deposit")
        self.initial_deposit_entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, "Initial Deposit"))
        self.initial_deposit_entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, "Initial Deposit"))
        self.initial_deposit_entry.pack(pady=12, padx=10)

        button = Button(master=frame, text='Create', command=self.on_confirm_button_click, bg="#2ECC71", fg="white")
        button.pack(pady=12, padx=10)

    def on_entry_focus_in(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")

    def on_entry_focus_out(self, event, placeholder):
        if not event.widget.get():
            event.widget.insert(0, placeholder)

    def on_confirm_button_click(self):
        username = self.user_entry.get()
        password = self.user_pass.get()
        confirm_password = self.confirm_pass.get()
        initial_deposit = self.initial_deposit_entry.get()

        try:
            self.bank_db.create_account(username, password, confirm_password, initial_deposit)
            messagebox.showinfo("Account Created", "Account has been successfully created!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = Tk()
    BankApp(root)
    root.mainloop()
