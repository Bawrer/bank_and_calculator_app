import sqlite3
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class DatabaseHandler:
    def __init__(self, db_file="bankapp.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                balance REAL NOT NULL,
                account_number TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def remove_user(self, account_number):
        try:
            self.cursor.execute("DELETE FROM users WHERE account_number=?", (account_number,))
            self.conn.commit()
            messagebox.showinfo("User Removed", f"User with account number {account_number} has been removed successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error removing user: {e}")

class AdminPage:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def view_all_users(self):
        users = self.db_handler.get_all_users()
        return users

    def remove_user(self, account_number):
        self.db_handler.remove_user(account_number)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ADMIN HOMEPAGE")
        self.geometry("600x300")

        self.accountNumberEntry = ctk.CTkEntry(self)
        self.accountNumberEntry.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

        self.removeUserButton = ctk.CTkButton(self, text="Remove User", command=self.remove_user_button_click)
        self.removeUserButton.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

        self.viewAllUsersButton = ctk.CTkButton(self, text="View All Users", command=self.view_all_users_button_click)
        self.viewAllUsersButton.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        self.logoutButton = ctk.CTkButton(self, text="Logout", command=self.logout_button_click)
        self.logoutButton.grid(row=6, column=2, padx=20, pady=20, sticky="ew")

        self.displayBox = ctk.CTkTextbox(self, width=200, height=100)
        self.displayBox.grid(row=7, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

    def remove_user_button_click(self):
        account_number = self.accountNumberEntry.get()
        if account_number.strip() != "":
            admin_page.remove_user(account_number)
            self.accountNumberEntry.delete(0, "end")  # Clear the entry after removal
        else:
            messagebox.showerror("Error", "Invalid account number. Please try again.")

    def view_all_users_button_click(self):
        users = admin_page.view_all_users()
        self.displayBox.delete("1.0", "end")
        for user in users:
            user_info = f"Username: {user[1]}, Account Number: {user[4]}, Balance: R{user[3]}\n"
            self.displayBox.insert("end", user_info)
        if not users:
            messagebox.showinfo("No Users", "There are no users in the database.")

    def logout_button_click(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            print("Admin logout successful.")
            self.destroy()

if __name__ == "__main__":
    db_handler = DatabaseHandler()
    admin_page = AdminPage(db_handler)
    app = App()
    app.mainloop()
