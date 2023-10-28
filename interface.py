import tkinter as tk
from tkinter import messagebox
import ast

window = tk.Tk()
window.title("SignUp | NoMorePass")
window.geometry("925x550+300+200")
window.config(bg="#fff")
window.resizable(False, False)


frame = tk.Frame(window, width=350, height=400, bg="#fff")
frame.place(x=480, y=50)

heading = tk.Label(
    frame,
    text="Sign Up",
    fg="#57a1f8",
    bg="white",
    font=("Microsoft Yahei UI Light", 23, "bold"),
)

heading.place(x=100, y=5)


###### -----  Username info ----- #####
def on_username_enter(e):
    user.delete(0, "end")


def on_username_leave(e):
    if user.get() == "":
        user.insert(0, "Username")


user = tk.Entry(
    frame,
    width=25,
    fg="black",
    border=0,
    bg="white",
    font=(
        "Microsoft Yahei UI Light",
        11,
    ),
)

user.place(x=30, y=80)
user.insert(0, "Username")
user.bind("<FocusIn>", on_username_enter)
user.bind("<FocusOut>", on_username_leave)

tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)


###### ----- Email Info ----- #####
def on_email_enter(e):
    email.delete(0, "end")


def on_email_leave(e):
    if email.get() == "":
        email.insert(0, "Email Address")


email = tk.Entry(
    frame,
    width=25,
    fg="black",
    border=0,
    bg="white",
    font=(
        "Microsoft Yahei UI Light",
        11,
    ),
)

email.place(x=30, y=150)
email.insert(0, "Email Address")
email.bind("<FocusIn>", on_email_enter)
email.bind("<FocusOut>", on_email_leave)

tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)


###### -----  Password info ----- #####
def on_password_enter(e):
    password.delete(0, "end")
    password.configure(show="*")


def on_password_leave(e):
    if password.get() == "":
        password.insert(0, "Password")
        password.configure(show="")


password = tk.Entry(
    frame,
    width=25,
    fg="black",
    border=0,
    bg="white",
    font=(
        "Microsoft Yahei UI Light",
        11,
    ),
)

password.place(x=30, y=220)
password.insert(0, "Password")
password.bind("<FocusIn>", on_password_enter)
password.bind("<FocusOut>", on_password_leave)

tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=247)


###### -----  Confirm Password info ----- #####
def on_confirm_password_enter(e):
    confirm_password.delete(0, "end")
    confirm_password.configure(show="*")


def on_confirm_password_leave(e):
    if confirm_password.get() == "":
        confirm_password.insert(0, "Confirm Password")
        confirm_password.configure(show="")


confirm_password = tk.Entry(
    frame,
    width=25,
    fg="black",
    border=0,
    bg="white",
    font=(
        "Microsoft Yahei UI Light",
        11,
    ),
)

confirm_password.place(x=30, y=290)
confirm_password.insert(0, "Confirm Password")
confirm_password.bind("<FocusIn>", on_confirm_password_enter)
confirm_password.bind("<FocusOut>", on_confirm_password_leave)

tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=317)

# ----- Button -----
tk.Button(
    frame, width=39, pady=7, text="Sign Up", bg="#57a1f8", fg="white", border=0,
    cursor='hand2').place(x=35, y=340)

account_exist_label = tk.Label(
    frame,
    text="I have an account",
    fg="black",
    bg="white",
    font=("Microsoft YaHei UI Light", 9),
)
account_exist_label.place(x=90, y=380)

signin_link = tk.Button(
    frame, width=6, text="Sign In", border=0, bg="white", cursor="hand2", fg="#57a1f8"
)
signin_link.place(x=200, y=380)


window.mainloop()
