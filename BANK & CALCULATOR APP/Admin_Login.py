# Admin_Login.py

import subprocess
from tkinter import messagebox
import bcrypt
import customtkinter as ctk
import sqlite3
from Admin_Page import AdminPage, AppAdmin, DatabaseHandler

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ADMIN")
        self.geometry("400x400")

        label = ctk.CTkLabel(self, text="Admin LOGIN")
        label.pack(pady=20)

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        label = ctk.CTkLabel(master=frame, text='ENTER ADMIN DETAILS')
        label.pack(pady=12, padx=10)

        user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
        user_entry.pack(pady=12, padx=10)

        user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
        user_pass.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='Login', command=lambda: login(user_entry.get(), user_pass.get()))
        button.pack(pady=12, padx=10)

        self.db_handler = DatabaseHandler()

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

        def login(username_entry, password_entry):
            entered_username = username_entry
            entered_password = password_entry

            admin_credentials = get_admin_credentials()
            if admin_credentials and entered_username == admin_credentials[0] and bcrypt.checkpw(entered_password.encode("utf-8"), admin_credentials[1].encode("utf-8")):
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                open_admin_page(self.db_handler)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

        def open_admin_page(db_handler):
            try:
                admin_page = AdminPage(db_handler)
                app_admin = AppAdmin(admin_page)
                app_admin.mainloop()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Admin Page: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
