# Admin_Page.py

import sqlite3
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")

class DatabaseHandler:
    def __init__(self, db_file="bankapp.db"):
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            raise  # Raise the exception to indicate the failure

    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    account_number TEXT PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    balance REAL
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )
            ''')
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise  # Raise the exception to indicate the failure

    def get_all_users(self):
        try:
            self.cursor.execute("SELECT account_number, username, balance FROM accounts")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing SELECT query: {e}")
            messagebox.showerror("Database Error", f"Error fetching users: {e}")
            raise  # Raise the exception to indicate the failure

    def remove_user(self, account_number):
        try:
            # Check if the account number exists before attempting to remove
            self.cursor.execute("SELECT * FROM accounts WHERE account_number=?", (account_number,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                # Account number exists, proceed with removal
                self.cursor.execute("DELETE FROM accounts WHERE account_number=?", (account_number,))
                self.conn.commit()
                print(f"User with account number {account_number} has been removed successfully.")
                messagebox.showinfo("User Removed", f"User with account number {account_number} has been removed successfully.")
            else:
                # Account number not found in the database
                print(f"User with account number {account_number} not found in the database.")
                messagebox.showerror("User Not Found", f"User with account number {account_number} not found in the database.")

            # Return the updated list of users after the deletion
            return self.get_all_users()
        except sqlite3.Error as e:
            print(f"Error removing user: {e}")
            messagebox.showerror("Database Error", f"Error removing user: {e}")
            raise  # Raise the exception to indicate the failure

class AdminPage:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def view_all_users(self):
        return self.db_handler.get_all_users()

    def remove_user(self, account_number):
        return self.db_handler.remove_user(account_number)

class AppAdmin(ctk.CTk):
    def __init__(self, admin_page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ADMIN HOMEPAGE")
        self.geometry("600x300")

        # Set background color to black
        self.configure(bg="black")

        self.admin_page = admin_page

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
        print("Remove User button clicked.")
        account_number = self.accountNumberEntry.get()
        print(f"Account number entered: {account_number}")
        if account_number.strip() != "":
            try:
                # Fetch the updated list of users after the removal
                updated_users = self.admin_page.remove_user(account_number)

                self.accountNumberEntry.delete(0, "end")  # Clear the entry after removal

                # Display the updated list of users in the console
                print(f"Updated users: {updated_users}")
            except Exception as e:
                print(f"Error removing user: {e}")
                messagebox.showerror("Error", f"An error occurred while removing the user. Please check the console for details.")
        else:
            messagebox.showerror("Error", "Invalid account number. Please try again.")

    def view_all_users_button_click(self):
        print("View All Users button clicked.")
        try:
            # Fetch the current list of users
            users = self.admin_page.view_all_users()
            print(f"Retrieved users: {users}")
            self.displayBox.delete("1.0", "end")

            if users:
                for user in users:
                    user_info = f"Account Number: {user[0]}, Username: {user[1]}, Balance: R{user[2]:.2f}\n"
                    self.displayBox.insert("end", user_info)
            else:
                messagebox.showinfo("No Users", "There are no users in the database.")
        except Exception as e:
            print(f"Error in view_all_users_button_click: {e}")
            messagebox.showerror("Error", f"An error occurred while fetching users. Please check the console for details.")

    def logout_button_click(self):
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            print("Admin logout successful.")
            self.destroy()

if __name__ == "__main__":
    try:
        db_handler = DatabaseHandler()
        admin_page = AdminPage(db_handler)
        app_admin = AppAdmin(admin_page)
        app_admin.mainloop()
    except Exception as e:
        print(f"Unhandled exception: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
