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

SCREEN_SIZE = "700x550"
MAIN_COLOR = "#A45EE5"
SECOND_COLOR = "#090909"
TEXT_COLOR = "#FFF"
ENTRY_WIDTH = 50
VERSION = "2.0.0"

current_date = datetime.now()
characters = string.ascii_letters + string.digits
http_selections = ["http://", "https://"]


def generate_key():
    return Fernet.generate_key()


def encrypt_password(key, password):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()


def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()


key = generate_key()


def add_login_entry():
    # gather all entries
    http_selection = http_var.get()
    website = website_entry.get()
    title = title_entry.get()
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    favorite = favorites_check.get()
    notes = entry_notes_box.get("1.0", "end")

    if not title:
        title = "Not Entered"
    if not username:
        username = email
    if notes and len(notes) > 200:
        notes = notes[:201]

    if website and email and password:
        encrypted_password = encrypt_password(key, password)

    else:
        messagebox.showerror(
            "All Fields Required", "Website, Email, and Password Fields Required."
        )


def generate_new_password():
    """Generate new password based on number of characters from spinbox."""
    characters_to_generate = int(characters_box.get())
    new_password = "".join(
        random.choice(characters) for _ in range(characters_to_generate)
    )

    # add to password entry box
    password_entry.delete(0, "end")
    password_entry.insert(0, new_password)


def clear_entries():
    for widget in frame.children.values():
        if isinstance(widget, tk.Entry):
            widget.delete(0, "end")
        elif isinstance(widget, tk.Checkbutton):
            widget.deselect()
        elif isinstance(widget, tk.Text):
            widget.delete("1.0", "end")


window = tk.Tk()
window.title("NoMorePass | Password Manager")
window.configure(bg=MAIN_COLOR)

# title frame
title_frame = tk.Frame(window, bg=SECOND_COLOR)
title_frame.grid(row=0, column=0, padx=25, pady=10)

# main frame
frame = tk.Frame(window, bg=SECOND_COLOR)
frame.grid(row=1, column=0, padx=10, pady=10)

# menu frame
menu_frame = tk.Frame(window, background=MAIN_COLOR)
menu_frame.grid(row=2, column=0, padx=10, pady=10)

# ============= Title and Instructions ============
instructions = """Use the entry fields to add, search, update and delete login entries. 
                  The following fields are required to add a password: Website Url, Email, and Password.
                  Generate a password by choosing amount of characters then clicking 'Generate Password.'"""
copyright_statement = f"""NoMorePass Password Manager V{VERSION}. Created by Isaiah Vickers. Copyright © {current_date.strftime('%Y')} by 8iVisions. All Rights Reserved."""

title_label = tk.Label(
    title_frame,
    text="Password Manager",
    font=(None, 20),
    bg=SECOND_COLOR,
    fg=TEXT_COLOR,
)
instructions_label = tk.Label(
    title_frame, text=instructions, bg=SECOND_COLOR, fg=TEXT_COLOR
)
title_label.grid(row=0, column=0, padx=10, pady=5)
instructions_label.grid(row=1, column=0, padx=50, pady=5)

# ============= Entries ====================
http_var = StringVar()
http_var.set("https://")
http_selector = ttk.Combobox(
    frame, textvariable=http_var, width=10, values=[p for p in http_selections]
)
http_selector.grid(row=0, column=1, padx=10, pady=5, sticky="w")


website_label = tk.Label(frame, text="Website Url:", bg=SECOND_COLOR, fg=TEXT_COLOR)
website_entry = tk.Entry(frame, width=ENTRY_WIDTH - 15)
website_label.grid(row=0, column=0, padx=10, pady=10)
website_entry.grid(row=0, column=1, padx=100, pady=5, sticky="w")

title_label = tk.Label(frame, text="Title:", bg=SECOND_COLOR, fg=TEXT_COLOR)
title_entry = tk.Entry(frame, width=ENTRY_WIDTH)
title_label.grid(row=1, column=0, padx=10, pady=10)
title_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

username_label = tk.Label(frame, text="Username:", bg=SECOND_COLOR, fg=TEXT_COLOR)
username_entry = tk.Entry(frame, width=ENTRY_WIDTH)
username_label.grid(row=2, column=0, padx=10, pady=10)
username_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

email_label = tk.Label(frame, text="Email Address:", bg=SECOND_COLOR, fg=TEXT_COLOR)
email_entry = tk.Entry(frame, width=ENTRY_WIDTH)
email_label.grid(row=3, column=0, padx=10, pady=10)
email_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

password_label = tk.Label(frame, text="Password:", bg=SECOND_COLOR, fg=TEXT_COLOR)
password_entry = tk.Entry(frame, width=ENTRY_WIDTH)
password_label.grid(row=4, column=0, padx=10, pady=10)
password_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

entry_notes_label = tk.Label(
    frame, text="Add Note: (max 200 char)", bg=SECOND_COLOR, fg=TEXT_COLOR
)
entry_notes_box = tk.Text(frame, width=ENTRY_WIDTH - 12, height=5)
entry_notes_label.grid(row=5, column=0, padx=10, pady=10)
entry_notes_box.grid(row=5, column=1, padx=10, pady=10, sticky="w")

favorites_check = BooleanVar()
add_to_favorites_check = tk.Checkbutton(
    frame,
    text="Add to My Favorites",
    onvalue=True,
    offvalue=False,
    bg=SECOND_COLOR,
    fg=TEXT_COLOR,
    selectcolor="black",
    variable=favorites_check,
)
add_to_favorites_check.grid(row=6, column=1, padx=10, pady=5)

characters_box = tk.Spinbox(frame, from_=4, to=20)
characters_box.grid(row=2, column=2, padx=10, pady=5, sticky="w")
password_generator_button = tk.Button(
    frame,
    text="Generate Password",
    bg=MAIN_COLOR,
    fg=SECOND_COLOR,
    command=generate_new_password,
)
password_generator_button.grid(row=3, column=2, padx=10, pady=5, sticky="w")

clear_all_button = tk.Button(
    frame, text="Clear All", bg=MAIN_COLOR, fg=SECOND_COLOR, command=clear_entries
)
clear_all_button.grid(row=4, column=2, padx=10, pady=5, sticky="w")
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
    menu_frame,
    text="ADD",
    bg=SECOND_COLOR,
    fg=TEXT_COLOR,
    width=15,
    command=add_login_entry,
)
find_button = tk.Button(
    menu_frame, text="FIND", bg=SECOND_COLOR, fg=TEXT_COLOR, width=15
)
update_button = tk.Button(
    menu_frame, text="UPDATE", bg=SECOND_COLOR, fg=TEXT_COLOR, width=15
)
delete_button = tk.Button(
    menu_frame, text="DELETE", bg=SECOND_COLOR, fg=TEXT_COLOR, width=15
)
export_button = tk.Button(
    menu_frame, text="EXPORT", bg=SECOND_COLOR, fg=TEXT_COLOR, width=15
)

add_button.grid(row=0, column=0, padx=5, pady=5)
find_button.grid(row=0, column=1, padx=5, pady=5)
update_button.grid(row=0, column=2, padx=5, pady=5)
delete_button.grid(row=0, column=3, padx=5, pady=5)
export_button.grid(row=0, column=4, padx=5, pady=5)

copyright_label = tk.Label(
    window, text=copyright_statement, bg=MAIN_COLOR, font=(None, 7)
)
copyright_label.grid(row=3, column=0, padx=10, pady=10)

window.resizable(False, False)
window.mainloop()
