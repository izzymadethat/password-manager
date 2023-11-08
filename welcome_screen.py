import tkinter as tk
from tkinter import ttk  # Import ttk module
from tkinter import BooleanVar, StringVar
from tkinter import messagebox
from datetime import datetime
from cryptography.fernet import Fernet
import random
import string
import re
import database as db


class WelcomeScreen:
    """Login and Signup screen"""

    def __init__(self):
        self.MAIN_COLOR = "#A45EE5"
        self.SECOND_COLOR = "#090909"
        self.TEXT_COLOR = "#FFF"
        self.ENTRY_WIDTH = 50
        self.successful_login = False
        self.signup_instructions = """Signup to start securely storing your passwords.
        \nCreate a password that's hard for someone to remember."""

    def login_user(self) -> bool:
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        if email != "Email Address" and password != "Master Password":
            valid_login = db.authenticate_user(email, password)
            if valid_login:
                self.successful_login = True
                return True
            else:
                messagebox.showwarning('User does not exist', 'User does not exist.\nPlease correct login or signup.')
        else:
            messagebox.showerror('No Information added', 'Please Enter Email & Password to login')

    def reset_fields(self):
        self.login_email_entry.delete(0, "end")
        self.login_password_entry.delete(0, "end")
        self.signup_entry.delete(0, "end")
        self.signup_password_entry.delete(0, "end")
        self.signup_password_confirmation_entry.delete(0, "end")

        self.login_email_entry.insert(0, "Email Address")
        self.login_password_entry.insert(0, "Master Password")
        self.signup_entry.insert(0, "Email Address")
        self.signup_password_entry.insert(0, "Master Password")
        self.signup_password_confirmation_entry.insert(0, "Master Password")

        if self.hide_password.get():
            self.hide_password.set(False)

    def check_if_valid_email(self, email):
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(email_pattern, email):
            return True

        return False

    def sign_user_up(self) -> bool:
        email = self.signup_entry.get()
        password = self.signup_password_entry.get()
        pw_confirmation = self.signup_password_confirmation_entry.get()

        if email != "Email Address" and password != "Master Password" and pw_confirmation != "Confirm Master Password":

            email_validated = self.check_if_valid_email(email)
            if email_validated:
                if password == pw_confirmation:
                    valid_login = db.check_if_email_exists(email)
                    if not valid_login:
                        db.create_user_upon_signup(email, password)
                        messagebox.showinfo("Succesful", "Welcome! You can now sign in.")
                        self.reset_fields()
                    else:
                        messagebox.showwarning("User exists", "Email already exists")
                        self.reset_fields()
                else:
                    messagebox.showerror('Mismatched Passwords', 'Passwords do not match.')
            else:
                messagebox.showerror('Invalid Email Format', 'Please enter a valid email')
        else:
            messagebox.showerror('No Information added', 'Please Enter All Email & Password to signup')

    def toggle_password_visibility(self, password_widgets):
        if self.hide_password.get():
            for widget in password_widgets:
                if widget.get() != "Master Password" and widget.get() != "Confirm Master Password":
                    widget.config(show="*")
        else:
            for widget in password_widgets:
                widget.config(show="")

    def on_enter(self, e, widget, placeholder_text):
        if widget.get() == placeholder_text:
            widget.delete(0, "end")
        elif widget == self.login_password_entry:
            check = self.hide_password.get()
            if check:
                widget.config(show="*")

    def on_exit(self, e, widget, placeholder):
        if widget.get() == "":
            if placeholder == "Master Password" or placeholder == "Confirm Master Password":
                widget.insert(0, placeholder)
                widget.config(show="")
            else:
                widget.insert(0, placeholder)

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("NoMorePass | Login or SignUp")
        self.window.configure(bg=self.MAIN_COLOR)

        self.title_frame = tk.Frame(self.window)
        self.title_frame.grid(row=0, column=0, padx=10, pady=10)
        self.title = tk.Label(
            self.title_frame,
            text="NoMorePass\nSecure Password Manager",
            bg=self.MAIN_COLOR,
            font=(None, 15),
        )
        self.title.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # ------------------ Login Section --------------------------
        self.login_frame = tk.Frame(self.window, bg=self.SECOND_COLOR)
        self.login_frame.grid(row=1, column=0, padx=10, pady=10)

        self.login_title = tk.Label(
            self.login_frame,
            text="Login",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            font=(None, 12),
        )
        self.login_title.grid(row=0, column=0, columnspan=2, padx=(5, 10), pady=5)

        # Email
        self.login_email_label = tk.Label(
            self.login_frame,
            text="Email:",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.login_email_entry = tk.Entry(self.login_frame, width=self.ENTRY_WIDTH - 15)
        self.login_email_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.login_email_entry.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="w")

        self.login_email_entry.insert(0, "Email Address")
        self.login_email_entry.bind(
            "<FocusIn>",
            lambda e: self.on_enter(e, self.login_email_entry, "Email Address"),
        )
        self.login_email_entry.bind(
            "<FocusOut>",
            lambda e: self.on_exit(e, self.login_email_entry, "Email Address"),
        )

        # Password
        self.login_password_label = tk.Label(
            self.login_frame,
            text="Master Password:",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.login_password_label.grid(row=2, column=0, padx=(5, 10), pady=5, sticky="w")
        self.login_password_entry = tk.Entry(
            self.login_frame,
            width=self.ENTRY_WIDTH - 15,
        )
        self.login_password_entry.grid(
            row=2, column=1, padx=(5, 10), pady=(5, 15), sticky="w"
        )
        self.login_password_entry.bind(
            "<FocusIn>",
            lambda e: self.on_enter(e, self.login_password_entry, "Master Password"),
        )
        self.login_password_entry.bind(
            "<FocusOut>",
            lambda e: self.on_exit(e, self.login_password_entry, "Master Password"),
        )

        self.login_password_entry.insert(0, "Master Password")


        self.login_button = tk.Button(
            self.login_frame,
            text="Login",
            bg=self.MAIN_COLOR,
            fg=self.SECOND_COLOR,
            width=15,
            command=self.login_user,
        )
        self.login_button.grid(row=4, column=1, columnspan=2, padx=(5, 10), pady=(5, 15), sticky="w")

        # ------------------ Sign Up Section ------------------------
        self.signup_frame = tk.Frame(self.window, bg=self.SECOND_COLOR)
        self.signup_frame.grid(row=2, column=0, padx=10, pady=10)

        self.signup_title = tk.Label(
            self.signup_frame,
            text="Sign Up",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            font=(None, 12),
        )
        self.signup_title.grid(row=0, column=0, columnspan=2, padx=(5, 10), pady=5)

        self.signup_text = tk.Label(
            self.signup_frame,
            text=self.signup_instructions,
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            font=(None, 8),
        )
        self.signup_text.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.signup_label = tk.Label(
            self.signup_frame,
            text="Email:",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.signup_entry = tk.Entry(self.signup_frame, width=self.ENTRY_WIDTH - 15)
        self.signup_label.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.signup_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="w")

        self.signup_entry.insert(0, "Email Address")
        self.signup_entry.bind(
            "<FocusIn>",
            lambda e: self.on_enter(e, self.signup_entry, "Email Address"),
        )
        self.signup_entry.bind(
            "<FocusOut>",
            lambda e: self.on_exit(e, self.signup_entry, "Email Address"),
        )

        self.signup_password_label = tk.Label(
            self.signup_frame,
            text="Create a Master Password:",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.signup_password_label.grid(row=3, column=0, padx=(5, 10), pady=5, sticky="w")
        self.signup_password_entry = tk.Entry(
            self.signup_frame, width=self.ENTRY_WIDTH - 15,
        )
        self.signup_password_entry.grid(row=3, column=1, padx=(5, 10), pady=(5, 15), sticky="w")

        self.signup_password_entry.insert(0, "Master Password")
        self.signup_password_entry.bind(
            "<FocusIn>",
            lambda e: self.on_enter(e, self.signup_password_entry, "Master Password"),
        )
        self.signup_password_entry.bind(
            "<FocusOut>",
            lambda e: self.on_exit(e, self.signup_password_entry, "Master Password"),
        )

        self.signup_password_confirmation_label = tk.Label(
            self.signup_frame,
            text="Confirm Master Password:",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.signup_password_confirmation_label.grid(row=4, column=0, padx=(5, 10), pady=5, sticky="w")
        self.signup_password_confirmation_entry = tk.Entry(
            self.signup_frame, width=self.ENTRY_WIDTH - 15,
        )
        self.signup_password_confirmation_entry.grid(row=4, column=1, padx=(5, 10), pady=(5, 15), sticky="w")

        self.signup_password_confirmation_entry.insert(0, "Confirm Master Password")
        self.signup_password_confirmation_entry.bind(
            "<FocusIn>",
            lambda e: self.on_enter(e, self.signup_password_confirmation_entry, "Confirm Master Password"),
        )
        self.signup_password_confirmation_entry.bind(
            "<FocusOut>",
            lambda e: self.on_exit(e, self.signup_password_confirmation_entry, "Confirm Master Password"),
        )


        # Option to show password
        self.hide_password = BooleanVar()
        self.password_visibility_check = tk.Checkbutton(
            self.signup_frame,
            text="Hide All Passwords",
            variable=self.hide_password,
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            onvalue=True,
            offvalue=False,
            selectcolor=self.SECOND_COLOR,
            command=lambda: self.toggle_password_visibility(
                [self.login_password_entry, self.signup_password_entry, self.signup_password_confirmation_entry]
            ),  # Attach the toggle function
        )
        self.password_visibility_check.grid(
            row=6, column=1, padx=(5, 10), pady=(5, 15), sticky="w"
        )

        self.signup_button = tk.Button(
            self.signup_frame,
            text="Start Storing Passwords",
            bg=self.MAIN_COLOR,
            fg=self.SECOND_COLOR,
            width=25,
            command=self.sign_user_up,
        )
        self.signup_button.grid(row=7, column=1, columnspan=2, padx=(5, 10), pady=(5, 15), sticky="w")

        self.window.resizable(False, False)
        self.window.mainloop()

    def run(self):
        self.create_gui()

    def destroy_(self):
        self.window.destroy()


app = WelcomeScreen()
app.run()
