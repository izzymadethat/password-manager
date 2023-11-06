"""
Password Manager App: Version 2.0.0
New Clean, Simple, and Better GUI
Securely store and retrieve passwords for user

Functions:
    Add user password entry: Website, Title, Username/Email, Password
    Encrypt password for database storage
    Decrypt password then retrieve information when user calls for it
    Generate a random password for user if needed
    Copy username or password for user to retrieve
    Edit password information stored in database then update database
    Go to site with login information entered
    Export saved passwords to CSV or JSON

Technical Requirements:
    Python: Main programming language
    Tkinter: GUI library
    cryptography.Fernet: Encryption and Decryption
    pymongo: Python library to handle MongoDb database functions
    datetime: Capture current date and time for database records and entries
    random: library to generate random password
    string: library to use of all characters a-zA-Z and digits 0-9 without having to type it

Database Layout (for each password entry):
    {
        "id": (generated by mongoDb) # get id upon entering,
        "website": "http(s)://website.com",
        "title": User-entered title -or- name of website if blank,
        "username": "myusername" -or- "myemail@email.com" if blank,
        "email": "myemail@email.com",
        "password": "mypassword",
        "favorited": true/false,
        "entry_notes": "User's description of password, they can store up to 200 char about their entry"
        "last_modified": "01-01-2000" # date of entry or date updated
    }

    (for each user):
    {
        "id": (generated user id),
        "first_name": "John",
        "last_name": "Doe",
        "username": "myusername",
        "email": "myemail@email.com",
        "password": "mypassword",
        "login_entries": {document of all saved passwords},
        "last_login_session": "01-01-2000 12:00:00UTC"
    }

Version 2.0.0: Created: 11/4/2023 by Isaiah Vickers

"""

import tkinter as tk
from tkinter import ttk
from tkinter import BooleanVar, StringVar
from tkinter import messagebox
from datetime import datetime
from cryptography.fernet import Fernet
import random
import string
import re


class PasswordManager:
    def __init__(self) -> None:
        self.MAIN_COLOR = "#A45EE5"
        self.SECOND_COLOR = "#090909"
        self.TEXT_COLOR = "#FFF"
        self.ENTRY_WIDTH = 50
        self.VERSION = "2.0.0"

        self.key = self.generate_key()
        self.passwords = []
        self.characters = string.ascii_letters + string.digits
        self.http_selections = ["http://", "https://"]

    def generate_key(self):
        return Fernet.generate_key()

    def encrypt_password(self, key, password):
        f = Fernet(key)
        return f.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        f = Fernet(self.key)
        return f.decrypt(encrypted_password.encode()).decode()

    def add_login_entry(self):
        # gather all entries
        http_selection = self.http_var.get()
        website = self.website_entry.get()
        title = self.title_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        favorite = self.favorites_check.get()
        notes = self.entry_notes_box.get("1.0", "end")

        valid_email = self.check_if_valid_email(email)

        if not title:
            title = "Not Entered"
        if not username and valid_email:
            username = email
        if notes and len(notes) > 200:
            notes = notes[:200]

        if website and valid_email and password:
            encrypted_password = self.encrypt_password(self.key, password)
            full_site = http_selection + website
            self.current_date = datetime.now().utcnow()
            formatted_date = self.current_date.strftime("%m/%d/%Y %H:%M:%S")
            messagebox.showinfo("Success", "Password added successfuly!")
            self.clear_entries()

        else:
            messagebox.showerror(
                "All Fields Required",
                "Website, Valid Email, and Password Fields Required.",
            )

    def check_if_valid_email(email: string) -> bool:
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(email_pattern, email):
            return True
        else:
            return False

    def generate_new_password(self):
        """Generate new password based on number of characters from spinbox."""
        characters_to_generate = int(self.characters_box.get())
        new_password = "".join(
            random.choice(self.characters) for _ in range(characters_to_generate)
        )

        # add to password entry box
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, new_password)

    def clear_entries(self):
        for widget in self.frame.children.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, "end")
            elif isinstance(widget, tk.Checkbutton):
                widget.deselect()
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", "end")
        self.http_var.set("https://")

    def find_query(database):
        pass

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("NoMorePass | Password Manager")
        self.window.configure(bg=self.MAIN_COLOR)

        # title frame
        self.title_frame = tk.Frame(self.window, bg=self.SECOND_COLOR)
        self.title_frame.grid(row=0, column=0, padx=25, pady=10)

        # main frame
        self.frame = tk.Frame(self.window, bg=self.SECOND_COLOR)
        self.frame.grid(row=1, column=0, padx=10, pady=10)

        # menu frame
        self.menu_frame = tk.Frame(self.window, background=self.MAIN_COLOR)
        self.menu_frame.grid(row=2, column=0, padx=10, pady=10)

        # ============= Title and Instructions ============
        self.current_date = datetime.now()
        self.instructions = """Use the entry fields to add, search, update and delete login entries.
                        The following fields are required to add a password: Website Url, Email, and Password.
                        Generate a password by choosing amount of characters then clicking 'Generate Password.'"""
        self.copyright_statement = f"""NoMorePass Password Manager V{self.VERSION}. Created by Isaiah Vickers. Copyright © {self.current_date.strftime('%Y')} by 8iVisions. All Rights Reserved."""

        self.title_label = tk.Label(
            self.title_frame,
            text="Password Manager",
            font=(None, 20),
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.instructions_label = tk.Label(
            self.title_frame,
            text=self.instructions,
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=5)
        self.instructions_label.grid(row=1, column=0, padx=50, pady=5)

        # ============= Entries ====================
        self.http_var = StringVar()
        self.http_var.set("https://")
        self.http_selector = ttk.Combobox(
            self.frame,
            textvariable=self.http_var,
            width=10,
            values=[p for p in self.http_selections],
        )
        self.http_selector.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.website_label = tk.Label(
            self.frame, text="Website Url:", bg=self.SECOND_COLOR, fg=self.TEXT_COLOR
        )
        self.website_entry = tk.Entry(self.frame, width=self.ENTRY_WIDTH - 15)
        self.website_label.grid(row=0, column=0, padx=10, pady=10)
        self.website_entry.grid(row=0, column=1, padx=100, pady=5, sticky="w")

        self.title_label = tk.Label(
            self.frame, text="Title:", bg=self.SECOND_COLOR, fg=self.TEXT_COLOR
        )
        self.title_entry = tk.Entry(self.frame, width=self.ENTRY_WIDTH)
        self.title_label.grid(row=1, column=0, padx=10, pady=10)
        self.title_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.username_label = tk.Label(
            self.frame, text="Username:", bg=self.SECOND_COLOR, fg=self.TEXT_COLOR
        )
        self.username_entry = tk.Entry(self.frame, width=self.ENTRY_WIDTH)
        self.username_label.grid(row=2, column=0, padx=10, pady=10)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.email_label = tk.Label(
            self.frame, text="Email Address:", bg=self.SECOND_COLOR, fg=self.TEXT_COLOR
        )
        self.email_entry = tk.Entry(self.frame, width=self.ENTRY_WIDTH)
        self.email_label.grid(row=3, column=0, padx=10, pady=10)
        self.email_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.password_label = tk.Label(
            self.frame, text="Password:", bg=self.SECOND_COLOR, fg=self.TEXT_COLOR
        )
        self.password_entry = tk.Entry(self.frame, width=self.ENTRY_WIDTH)
        self.password_label.grid(row=4, column=0, padx=10, pady=10)
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.entry_notes_label = tk.Label(
            self.frame,
            text="Add Note: (max 200 char)",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
        )
        self.entry_notes_box = tk.Text(
            self.frame, width=self.ENTRY_WIDTH - 12, height=5
        )
        self.entry_notes_label.grid(row=5, column=0, padx=10, pady=10)
        self.entry_notes_box.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.favorites_check = BooleanVar()
        self.add_to_favorites_check = tk.Checkbutton(
            self.frame,
            text="Add to My Favorites",
            onvalue=True,
            offvalue=False,
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            selectcolor="black",
            variable=self.favorites_check,
        )
        self.add_to_favorites_check.grid(row=6, column=1, padx=10, pady=5)

        self.characters_box = tk.Spinbox(self.frame, from_=4, to=20)
        self.characters_box.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.password_generator_button = tk.Button(
            self.frame,
            text="Generate Password",
            bg=self.MAIN_COLOR,
            fg=self.SECOND_COLOR,
            command=self.generate_new_password,
        )
        self.password_generator_button.grid(
            row=3, column=2, padx=10, pady=5, sticky="w"
        )

        self.clear_all_button = tk.Button(
            self.frame,
            text="Clear All",
            bg=self.MAIN_COLOR,
            fg=self.SECOND_COLOR,
            command=self.clear_entries,
        )
        self.clear_all_button.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        # ================== Menu Section ========================
        """
                                All buttons and their functions.

        Add: Encrpyt password then store new entry into database then msgbox password with id.
            Required fields to check: Website, Email, Password, msgbox if no exist.

        Find: Searches for entry once user enters data in fields.
            If found, the fields are populated with the user's information

        Update: Update user's information with whatever field has new information.
                Check if entry exists otherwise msgbox entry not found.

        Delete: Delete entry, user must use find to populate all boxes.
                Msgbox yes/no. If yes, delete entire password information from database

        Export: Msgbox yes/no. If yes, decrypt all passwords and export to csv

        """

        add_button = tk.Button(
            self.menu_frame,
            text="ADD",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            width=15,
            command=self.add_login_entry,
        )
        find_button = tk.Button(
            self.menu_frame,
            text="FIND",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            width=15,
        )
        update_button = tk.Button(
            self.menu_frame,
            text="UPDATE",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            width=15,
        )
        delete_button = tk.Button(
            self.menu_frame,
            text="DELETE",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            width=15,
        )
        export_button = tk.Button(
            self.menu_frame,
            text="EXPORT",
            bg=self.SECOND_COLOR,
            fg=self.TEXT_COLOR,
            width=15,
        )

        add_button.grid(row=0, column=0, padx=5, pady=5)
        find_button.grid(row=0, column=1, padx=5, pady=5)
        update_button.grid(row=0, column=2, padx=5, pady=5)
        delete_button.grid(row=0, column=3, padx=5, pady=5)
        export_button.grid(row=0, column=4, padx=5, pady=5)

        copyright_label = tk.Label(
            self.window,
            text=self.copyright_statement,
            bg=self.MAIN_COLOR,
            font=(None, 7),
        )
        copyright_label.grid(row=3, column=0, padx=10, pady=10)

        self.window.resizable(False, False)
        self.window.mainloop()

    def run(self):
        self.create_gui()


if __name__ == "__main__":
    app = PasswordManager()
    app.run()