from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter
import random
import string
import database as db
import csv
from datetime import datetime
import numpy as np
from openpyxl import Workbook
import pyperclip

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


def set_placeholder(word, num):
    for ph in range(0, 5):
        if ph == num:
            placeholder[ph].set(word)


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
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if username == "":
        username = email

    information = db.create_information(
        'test_passwords', [url, title, username, email, password, date])
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
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showwarning("No Item Selected", "Select a row to update.")
        return

    try:
        selected_id = str(tree.item(selected_item[0])['values'][0])
        url = str(url_entry.get())
        title = str(title_entry.get())
        username = str(username_entry.get())
        email = str(email_entry.get())
        password = str(password_entry.get())
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if url == "" and title == "" and username == "" and email == "" and password == "":
            messagebox.showwarning("Nothing to Update",
                                   "No information to update.")
            return
        if username == "":
            username = email

        updated = db.update_information(
            selected_id, url, title, username, email, password, date)

        if updated:
            clear_entry_boxes()
            messagebox.showinfo("Success", "Information successfully updated!")
            refresh_table()
    except Exception as e:
        print("Error:", str(e))
        messagebox.showerror("Error", "An error occurred while updating.")


def select():
    try:
        selected_item = tree.selection()[0]
        selected_id = str(tree.item(selected_item)['values'][0])
        selected_website = str(tree.item(selected_item)['values'][1])
        selected_title = str(tree.item(selected_item)['values'][2])
        selected_username = str(tree.item(selected_item)['values'][3])
        selected_email = str(tree.item(selected_item)['values'][4])
        selected_password = str(tree.item(selected_item)['values'][5])

        set_placeholder(selected_website, 0)
        set_placeholder(selected_title, 1)
        set_placeholder(selected_username, 2)
        set_placeholder(selected_email, 3)
        set_placeholder(selected_password, 4)
    except:
        messagebox.showwarning("No Item Selected", "Select a row to update.")


def copy():
    try:
        selected_item = tree.selection()[0]
        selected_password = str(tree.item(selected_item)['values'][5])

        pyperclip.copy(selected_password)

        messagebox.showinfo("", "Password Copied!")

    except:
        messagebox.showwarning(
            "No Item Selected", "Select an item to copy the password.")
        return


def delete():
    try:
        if tree.selection()[0]:
            confirmation = messagebox.askquestion(
                "Warning: Permanent Deletion", "DELETING this entry is PERMANENT!! Continue?")

            if confirmation == 'no':
                return
            else:
                selected_item = tree.selection()[0]
                selected_id = str(tree.item(selected_item)["values"][0])
                try:
                    db.delete_entry(selected_id)
                    messagebox.showinfo("Success", "Information Deleted")
                except Exception as e:
                    print("Error:", str(e))
                    messagebox.showerror(f"Error", "An error has occured.")
                refresh_table()
    except:
        messagebox.showwarning("No Item Selected", "Select a row to delete.")
        return


def find_query(entry, column):
    sql = f"SELECT * FROM test_passwords WHERE {column} LIKE '%{entry}%'"

    return sql


def find():
    website = str(url_entry.get())
    title = str(title_entry.get())
    username = str(username_entry.get())
    email = str(email_entry.get())
    password = str(password_entry.get())

    conn, c = db.connect()

    if website:
        sql = find_query(website, 'url')
    elif title:
        sql = find_query(title, 'title')
    elif username:
        sql = find_query(username, 'username')
    elif email:
        sql = find_query(email, 'email')
    elif password:
        sql = find_query(password, 'password')
    else:
        messagebox.showerror(
            "Nothing entered", "Fill one of the entries\nin order to find login information")
        return

    c.execute(sql)
    try:
        result = c.fetchall()
        for num in range(0, 5):
            set_placeholder(result[0][num], (num))
        conn.commit()
        conn.close()
    except:
        messagebox.showerror("No results", "Login not found.")


def show_export_window():
    top = Toplevel()
    top.title("Export to File")

    top.geometry("200x100")

    excel_check = tkinter.IntVar()
    csv_check = tkinter.IntVar()

    excel_checked = Checkbutton(
        top, text="Export to Excel", variable=excel_check, onvalue=1, offvalue=0)
    csv_checked = Checkbutton(
        top, text="Export to CSV", variable=csv_check, onvalue=1, offvalue=0)
    export_file_btn = Button(top, text="EXPORT FILE(S)", width=20,
                             borderwidth=3, bg=btn_color, fg='white', command=lambda: export_files(excel_check, csv_check, top))

    excel_checked.pack()
    csv_checked.pack()
    export_file_btn.pack()

    top.resizable(False, False)
    top.mainloop()


def export_files(excel_check, csv_check, top):
    date = str(datetime.now())
    date = date.replace(" ", "_")
    date = date.replace(":", '-')
    datefinal = date[:16]

    success_message = None

    try:
        if excel_check.get() == 1:
            file_path = filedialog.asksaveasfilename(
                initialfile=f"passwords_{datefinal}.xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            if file_path:
                export_to_excel(file_path)
                success_message = "Passwords saved successfully."

        if csv_check.get() == 1:
            file_path = filedialog.asksaveasfilename(
                initialfile=f"passwords_{datefinal}.csv",
                filetypes=[("CSV files", "*.csv")]
            )
            if file_path:
                export_to_csv(file_path)
                success_message = "Passwords saved successfully."

        if excel_check.get() == 0 and csv_check.get() == 0:
            messagebox.showerror("Nothing Selected",
                                 "Select at least one option")
            return

        if success_message:
            messagebox.showinfo("Success", success_message)
            top.destroy()

    except Exception as e:
        print("Error:", str(e))
        messagebox.showerror(
            "Save Error", "Something went wrong while saving...")


def export_to_csv(file):

    try:
        conn, c = db.connect()
        sql = f"SELECT rowid, * FROM test_passwords ORDER BY rowid DESC"

        c.execute(sql)
        dataraw = c.fetchall()
        date = str(datetime.now())
        date = date.replace(" ", "_")
        date = date.replace(":", '-')
        datefinal = date[:16]

        with open(file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "URL", "Title", "Username",
                            "Email", "Password", "Date"])
            for record in dataraw:
                writer.writerow(record)

        return True

    except Exception as e:
        print("Save error: " + str(e))
        return False


def export_to_excel(file):

    try:
        date = str(datetime.now())
        date = date.replace(" ", "_")
        date = date.replace(":", '-')
        datefinal = date[:16]

        data = db.read_all_data()

        wb = Workbook()
        ws = wb.active

        header = ["ID", "URL", "Title", "Username",
                  "Email", "Password", "Date"]
        ws.append(header)

        for row in data:
            ws.append(row)

        filepath = file
        wb.save(filepath)
        return True

    except Exception as e:
        print("Save error: " + str(e))
        return False

# def export_to_excel():
#     conn, c = db.connect()
#     sql = f"SELECT rowid, * FROM test_passwords ORDER BY rowid DESC"

#     c.execute(sql)
#     dataraw = c.fetchall()
#     date = str(datetime.now())
#     date = date.replace(" ", "_")
#     date = date.replace(":", '-')
#     datefinal = date[:16]

#     with open("passwords_"+datefinal+".csv", "w", newline='') as f:
#         writer = csv.writer(f, dialect='excel')

#         for record in dataraw:
#             writer.writerow(record)
#     messagebox.showinfo(
#         "Success", "Passwords saved successfully to "+datefinal+".csv")

#     conn.commit()
#     conn.close()

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
select_btn = Button(options_frame, text="SELECT", width=10,
                    borderwidth=3, bg=btn_color, fg='white', command=select)
delete_btn = Button(options_frame, text="DELETE", width=10,
                    borderwidth=3, bg=btn_color, fg='white', command=delete)
copy_btn = Button(options_frame, text="COPY", width=10,
                  borderwidth=3, bg=btn_color, fg='white', command=copy)
find_btn = Button(options_frame, text="FIND", width=10,
                  borderwidth=3, bg=btn_color, fg='white', command=find)
export_btn = Button(options_frame, text="EXPORT", width=10,
                    borderwidth=3, bg=btn_color, fg='white', command=show_export_window)

add_btn.grid(row=0, column=0, padx=5, pady=5)
select_btn.grid(row=0, column=1, padx=5, pady=5)
update_btn.grid(row=0, column=2, padx=5, pady=5)
delete_btn.grid(row=0, column=3, padx=5, pady=5)
copy_btn.grid(row=0, column=4, padx=5, pady=5)
find_btn.grid(row=0, column=5, padx=5, pady=5)
export_btn.grid(row=0, column=6, padx=5, pady=5)
# ======================================================================== #

# ========== Form section ==============

entries_frame = tkinter.LabelFrame(frame, text="Add/Edit Login", borderwidth=5)
entries_frame.grid(row=1, column=0, sticky='w',
                   padx=(50, 200), pady=20, ipadx=6)

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

# Password Generator and clear
pasword_generator_btn = Button(
    entries_frame, text="GENERATE PASSWORD", borderwidth=3,
    bg=btn_color, fg='white', command=get_a_password)
clear_btn = Button(
    entries_frame, text="CLEAR ALL", borderwidth=3,
    bg=btn_color, fg='white', command=clear_entry_boxes)
pasword_generator_btn.grid(row=0, column=3, padx=5, pady=5)
clear_btn.grid(row=1, column=3, padx=5, pady=5)

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
tree.column("Date", anchor=W, width=100)

tree.heading("ID", text="ID", anchor=W)
tree.heading("Url", text="Url", anchor=W)
tree.heading("Title", text="Title", anchor=W)
tree.heading("Username", text="Username", anchor=W)
tree.heading("Email", text="Email", anchor=W)
tree.heading("Password", text="Password", anchor=W)
tree.heading("Date", text="Last Modified", anchor=W)

tree.tag_configure('orow', background="#EEEEEE")
tree.pack()

refresh_table()

win.resizable(False, False)
win.mainloop()
