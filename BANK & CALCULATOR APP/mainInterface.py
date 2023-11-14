import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

class MainInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank App Main Interface")
        self.master.geometry("400x400")
        self.master.configure(bg="#2C3E50")  # Set the background color of the main window

        label = tk.Label(self.master, text="Welcome to the Bank App", font=("Helvetica", 16), bg="#2C3E50", fg="#ECF0F1")
        label.pack(pady=20)

        # Button to log in as a user
        user_button = tk.Button(self.master, text="Log in as User", command=self.login_as_user, bg="#2ECC71", fg="white")
        user_button.pack(pady=10)

        # Button to log in as an admin
        admin_button = tk.Button(self.master, text="Log in as Admin", command=self.login_as_admin,  bg="#3498DB", fg="white")
        admin_button.pack(pady=10)

        # Button to create a new account
        create_account_button = tk.Button(self.master, text="Create New Account", command=self.create_account, bg="#E74C3C", fg="white")
        create_account_button.pack(pady=10)

    def login_as_user(self):
        try:
            subprocess.run([sys.executable, "User_Login.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open User Login Page: {e}")

    def login_as_admin(self):
        try:
            subprocess.run([sys.executable, "Admin_Login.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Admin Login Page: {e}")

    def create_account(self):
        try:
            subprocess.run([sys.executable, "Create_Account.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Create Account Page: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    main_interface = MainInterface(root)
    root.mainloop()
