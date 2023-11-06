import tkinter as tk
from tkinter import ttk
from tkinter import BooleanVar, StringVar
from tkinter import messagebox
from datetime import datetime
from cryptography.fernet import Fernet
import random
import string
import re


class WelcomeScreen:
    """Login and Signup screen"""

    def __init__(self):
        self.MAIN_COLOR = "#A45EE5"
        self.SECOND_COLOR = "#090909"
        self.TEXT_COLOR = "#FFF"
        self.ENTRY_WIDTH = 50
        self.signup_instructions = """Signup to start securely storing your passwords.
        \nCreate a password that's hard for someone to remember."""

        self.key = self.generate_key()

    def generate_key(self):
        return Fernet.generate_key()

    def encrypt_password(self, key, password):
        f = Fernet(key)
        return f.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        f = Fernet(self.key)
        return f.decrypt(encrypted_password.encode()).decode()

    def toggle_password_visibility(self, password_widget):
        if (
            self.hide_password.get() and not password_widget.get() == "Master Password"
        ):  # if show password is checked
            password_widget.config(show="*")
        elif password_widget.get() == "Master Password" or password_widget.get() == "":
            password_widget.config(show="")
        else:  # if unchecked
            password_widget.config(show="")

    def on_enter(self, e, widget, placeholder_text):
        if widget.get() == placeholder_text:
            widget.delete(0, "end")
        elif widget == self.login_password_entry:
            check = self.hide_password.get()
            if check:
                widget.config(show="*")

    def on_exit(self, e, widget, placeholder):
        if widget.get() == "":
            if placeholder == "Master Password":
                widget.insert(0, placeholder)
                widget.config(show="")
            else:
                widget.insert(0, placeholder)

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("NoMorePass | Login or SignUp")
        self.window.configure(bg=self.MAIN_COLOR)

        self.title_frame = tk.Frame(self.window).grid(row=0, column=0, padx=10, pady=10)
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
        ).grid(row=0, column=0, columnspan=2, padx=(5, 10), pady=5)

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
        ).grid(row=2, column=0, padx=(5, 10), pady=5, sticky="w")
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

        # Option to show password
        self.hide_password = BooleanVar()
        self.password_visibility_check = tk.Checkbutton(
            self.login_frame,
            text="Hide Password",
            variable=self.hide_password,
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            onvalue=True,
            offvalue=False,
            selectcolor=self.SECOND_COLOR,
            command=lambda: self.toggle_password_visibility(
                self.login_password_entry
            ),  # Attach the toggle function
        )
        self.password_visibility_check.grid(
            row=3, column=1, padx=(5, 10), pady=(5, 15), sticky="w"
        )

        self.login_button = tk.Button(
            self.login_frame,
            text="Login",
            bg=self.MAIN_COLOR,
            fg=self.SECOND_COLOR,
            width=15,
        ).grid(row=4, column=1, columnspan=2, padx=(5, 10), pady=(5, 15), sticky="w")

        # ------------------ Sign Up Section ------------------------
        self.signup_frame = tk.Frame(self.window, bg=self.SECOND_COLOR)
        self.signup_frame.grid(row=2, column=0, padx=10, pady=10)

        self.signup_title = tk.Label(
            self.signup_frame,
            text="Sign Up",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            font=(None, 12),
        ).grid(row=0, column=0, columnspan=2, padx=(5, 10), pady=5)

        self.signup_text = tk.Label(
            self.signup_frame,
            text=self.signup_instructions,
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            font=(None, 8),
        ).grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.signup_label = tk.Label(
            self.signup_frame,
            text="Email:",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.signup_entry = tk.Entry(self.signup_frame, width=self.ENTRY_WIDTH - 15)
        self.signup_label.grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.signup_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="w")

        self.signup_password_label = tk.Label(
            self.signup_frame,
            text="Create a Master Password:",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        ).grid(row=3, column=0, padx=(5, 10), pady=5, sticky="w")
        self.signup_password_entry = tk.Entry(
            self.signup_frame, width=self.ENTRY_WIDTH - 15, show="*"
        ).grid(row=3, column=1, padx=(5, 10), pady=(5, 15), sticky="w")

        self.signup_password_confirmation_label = tk.Label(
            self.signup_frame,
            text="Confirm Master Password:",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        ).grid(row=4, column=0, padx=(5, 10), pady=5, sticky="w")
        self.signup_password_confirmation_entry = tk.Entry(
            self.signup_frame, width=self.ENTRY_WIDTH - 15, show="*"
        ).grid(row=4, column=1, padx=(5, 10), pady=(5, 15), sticky="w")
        self.signup_button = tk.Button(
            self.signup_frame,
            text="Start Storing Passwords",
            bg=self.MAIN_COLOR,
            fg=self.SECOND_COLOR,
            width=25,
        ).grid(row=5, column=1, columnspan=2, padx=(5, 10), pady=(5, 15), sticky="w")

        self.toggle_password_visibility(self.login_password_entry)

        self.window.resizable(False, False)
        self.window.mainloop()

    def run(self):
        self.create_gui()


app = WelcomeScreen()
app.run()
