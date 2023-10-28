from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random
import string
import database as db
import csv
from datetime import datetime
import numpy as np

win = tkinter.Tk()
win.title("NoMorePass | Dashboard")
win.geometry("720x640")
tree = ttk.Treeview(win, show='headings', height=20)
style = ttk.Style()

placeholder = ['', '', '', '', '']
entry_widgets = []
password_characters = string.ascii_letters + string.digits
password_length = 16

for i in range(0, 5):
    placeholder[i] = tkinter.StringVar()

frame = tkinter.Frame(win, bg='#02577A')
frame.pack()

# =========== Functions ===================

dummydata = [
    [1234, 'https://facebook.com', 'Facebook', 'izzy', 'izzy@me.com', 'test'],
    [123463, 'https://facebook2.com', 'Facebook', 'izzy', 'izzy@me.com', 'test'],
    [1237, 'https://facebook3.com', 'Facebook', 'izzy', 'izzy@me.com', 'test'],
    [123123, 'https://facebook4.com', 'Facebook', 'izzy', 'izzy@me.com', 'test'],
    [123123, 'https://facebook5.com', 'Facebook', 'izzy', 'izzy@me.com', 'test'],
    [21323, 'https://facebook6.com', 'Facebook', 'izzy', 'izzy@me.com', 'test'],
    [231453, 'https://facebook7.com', 'Facebook', 'izzy', 'izzy@me.com', 'test'],
    [87954674, 'https://facebook8.com', 'Facebook', 'izzy', 'izzy@me.com', 'test'],
]


def refresh_table():
    for data in tree.get_children():
        tree.delete(data)

    for array in db.read_all_data():
        tree.insert(parent='', index='end', iid=array,
                    text="", values=(array), tag="orow")
    tree.tag_configure('orow', background="#EEEEEE")
    tree.pack()


def generate_password():
    password = ''.join(random.choice(password_characters)
                       for _ in range(password_length))
    print(password)
    return str(password)


def get_a_password():
    """When random password generated, add into password entry box."""

    password = generate_password()

    password_entry.delete(0, "end")
    password_entry.insert(0, password)


def clear_entry_boxes():
    """Delete all entries on a successful add"""

    for entry in entry_widgets:
        entry.delete(0, "end")


def add_login():
    """"When the add button is pressed, add all data entered."""

    url = str(url_entry.get())
    title = str(title_entry.get())
    username = str(username_entry.get())
    email = str(email_entry.get())
    password = str(password_entry.get())

    if username == "":
        username = email

    information = db.create_information(
        'test_passwords', [url, title, username, email, password])
    try:
        if information:
            clear_entry_boxes()
            messagebox.showinfo("Success", "Information succesfully added!")
            refresh_table()
    except Exception as e:
        print("Error:", str(e))
        messagebox.showerror("Error", "Error while saving")


def update():
    selected_id = ""
    try:
        selected_item = tree.selection()[0]
        selected_id = str(tree.item(selected_item)['values'][0])
    except:
        messagebox.showwarning("No Item Selected", "Select a row to update.")

    print(selected_id)
    url = str(url_entry.get())
    title = str(title_entry.get())
    username = str(username_entry.get())
    email = str(email_entry.get())
    password = str(password_entry.get())

    if username == "":
        username = email

    updated = db.update_information(
        selected_id, url, title, username, email, password)

    try:
        if updated:
            clear_entry_boxes()
            messagebox.showinfo("Success", "Information succesfully updated!")
            refresh_table()
    except Exception as e:
        print("Error:", str(e))
        messagebox.showerror("Error", "Error while saving")


# CREATE DATABASE
# table = db.create_table("test_passwords",
#                         ('url', 'TEXT'),
#                         ('title', 'TEXT'),
#                         ('username', 'TEXT'),
#                         ('email', 'TEXT'),
#                         ('password', 'TEXT'))


# ========== Options section ==============
btn_color = "#196E78"
options_frame = tkinter.LabelFrame(frame, text="Manage", borderwidth=5)
options_frame.grid(row=0, column=0, sticky='w', padx=[
                   10, 200], pady=20, ipadx=[6])

add_btn = Button(options_frame, text="ADD", width=10,
                 borderwidth=3, bg=btn_color, fg='white', command=add_login)
update_btn = Button(options_frame, text="UPDATE", width=10,
                    borderwidth=3, bg=btn_color, fg='white', command=update)
delete_btn = Button(options_frame, text="DELETE", width=10,
                    borderwidth=3, bg=btn_color, fg='white')
copy_btn = Button(options_frame, text="COPY", width=10,
                  borderwidth=3, bg=btn_color, fg='white')
clear_btn = Button(options_frame, text="CLEAR", width=10,
                   borderwidth=3, bg=btn_color, fg='white')
export_btn = Button(options_frame, text="EXPORT", width=10,
                    borderwidth=3, bg=btn_color, fg='white')
save_btn = Button(options_frame, text="SAVE", width=10,
                  borderwidth=3, bg=btn_color, fg='white')

add_btn.grid(row=0, column=0, padx=5, pady=5)
update_btn.grid(row=0, column=1, padx=5, pady=5)
delete_btn.grid(row=0, column=2, padx=5, pady=5)
copy_btn.grid(row=0, column=3, padx=5, pady=5)
clear_btn.grid(row=0, column=4, padx=5, pady=5)
export_btn.grid(row=0, column=5, padx=5, pady=5)
save_btn.grid(row=0, column=6, padx=5, pady=5)
# ======================================================================== #

# ========== Form section ==============

entries_frame = tkinter.LabelFrame(frame, text="Add Login", borderwidth=5)
entries_frame.grid(row=1, column=0, sticky='w', padx=[
                   10, 200], pady=20, ipadx=[6])

# Labels
url_label = Label(entries_frame, text="URL", anchor="e", width=10)
title_label = Label(entries_frame, text="TITLE", anchor="e", width=10)
username_label = Label(entries_frame, text="USERNAME", anchor="e", width=10)
email_label = Label(entries_frame, text="EMAIL", anchor="e", width=10)
password_label = Label(entries_frame, text="PASSWORD", anchor="e", width=10)

url_label.grid(row=0, column=0, padx=10)
title_label.grid(row=1, column=0, padx=10)
username_label.grid(row=2, column=0, padx=10)
email_label.grid(row=3, column=0, padx=10)
password_label.grid(row=4, column=0, padx=10)

# Inputs
url_entry = Entry(entries_frame, width=50, textvariable=placeholder[0])
title_entry = Entry(entries_frame, width=50, textvariable=placeholder[1])
username_entry = Entry(entries_frame, width=50, textvariable=placeholder[2])
email_entry = Entry(entries_frame, width=50, textvariable=placeholder[3])
password_entry = Entry(entries_frame, width=50, textvariable=placeholder[4])

url_entry.grid(row=0, column=2, padx=10, pady=5)
title_entry.grid(row=1, column=2, padx=10, pady=5)
username_entry.grid(row=2, column=2, padx=10, pady=5)
email_entry.grid(row=3, column=2, padx=10, pady=5)
password_entry.grid(row=4, column=2, padx=10, pady=5)

entry_widgets.extend(
    [url_entry, title_entry, username_entry, email_entry, password_entry])

# Password Generator
pasword_generator_btn = Button(
    entries_frame, text="GENERATE PASSWORD", borderwidth=3,
    bg=btn_color, fg='white', command=get_a_password)
pasword_generator_btn.grid(row=0, column=3, padx=5, pady=5)

# ========== Tree section ==============
style.configure(win)
tree['columns'] = ("ID", "Url", "Title", "Username",
                   "Email", "Password", "Date")

tree.column("#0", width=0, stretch=NO)
tree.column("ID", anchor=W, width=70)
tree.column("Url", anchor=W, width=100)
tree.column("Title", anchor=W, width=100)
tree.column("Username", anchor=W, width=100)
tree.column("Email", anchor=W, width=100)
tree.column("Password", anchor=W, width=100)
tree.column("Date", anchor=W, width=150)

tree.heading("ID", text="ID", anchor=W)
tree.heading("Url", text="Url", anchor=W)
tree.heading("Title", text="Title", anchor=W)
tree.heading("Username", text="Username", anchor=W)
tree.heading("Email", text="Email", anchor=W)
tree.heading("Password", text="Password", anchor=W)
tree.heading("Date", text="Date", anchor=W)

tree.tag_configure('orow', background="#EEEEEE")
tree.pack()

refresh_table()

win.resizable(False, False)
win.mainloop()
