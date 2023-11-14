import subprocess
from tkinter import messagebox
import bcrypt
import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BankDatabase:
    def __init__(self, db_file="bank_database.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_table()
        self.create_admin()

    def create_table(self):
        # Create the 'accounts' table
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                username TEXT,
                password TEXT,
                balance REAL
            )
        ''')

        # Create the 'admins' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        self.conn.commit()

    def create_admin(self):
        # Create an admin user if it doesn't exist
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)",
            (
                "admin",
                bcrypt.hashpw("admin@123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            ),
        )
        self.conn.commit()

    def execute(self, *args, **kwargs):
        return self.conn.execute(*args, **kwargs)

def get_admin_credentials():
    conn = sqlite3.connect('bank_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM admins LIMIT 1")
    admin_data = cursor.fetchone()
    conn.close()

    if admin_data:
        return admin_data
    else:
        return None

bank_database = BankDatabase()
cursor = bank_database.execute("SELECT * FROM admins WHERE username=?", ("admin",))
admin_user = cursor.fetchone()

def login(username_entry, password_entry):
    entered_username = username_entry.get()
    entered_password = password_entry.get()

    if admin_user and bcrypt.checkpw(entered_password.encode("utf-8"), admin_user[2].encode("utf-8")):
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        open_admin_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

def open_admin_page():
    try:
        subprocess.run(["python", "Admin_Page.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Admin Page: {e}")

app = ctk.CTk()
app.geometry("400x400")
app.title("ADMIN")

label = ctk.CTkLabel(app, text="Admin LOGIN")
label.pack(pady=20)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='ENTER ADMIN DETAILS')
label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text='Login', command=lambda: login(user_entry.get(), user_pass.get()))
button.pack(pady=12, padx=10)

app.mainloop()
