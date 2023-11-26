import random
import string
import pyperclip
from tkinter import *
from tkinter import messagebox
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    password = ''.join(random.choices(password_characters, k=16))
    shuffled_password = ''.join(random.sample(password, len(password)))
    pw_entry.insert(0, shuffled_password)
    pyperclip.copy(shuffled_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    new_data = {
        web_entry.get(): {
            "email": em_entry.get(),
            "password": pw_entry.get()
        }
    }
    if len(web_entry.get()) == 0 or len(pw_entry.get()) == 0:
        messagebox.showwarning(title="Arererere", message="Please don't leave any fields empty!!")
    # else:
    #     is_ok = messagebox.askokcancel(title=web_entry.get(),
    #                                    message=f"These are the details entered: \nEmail: {em_entry.get()}"
    #                                            f"\n Password: {pw_entry.get()} \nIs this information OK to "
    #                                            f"save?")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            web_entry.delete(0, "end")
            pw_entry.delete(0, "end")


# ------------------------------ SEARCH ---------------------------------#
def search_password():
    if len(web_entry.get()):
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except (KeyError, FileNotFoundError):
            messagebox.showinfo(title="Error", message="The file you are looking for does not exist!")
        else:
            if web_entry.get() in data:
                json_em = data[web_entry.get()]["email"]
                json_pass = data[web_entry.get()]["password"]
                messagebox.showinfo(title="Info", message=f"Here are your credentials: \n \nEmail: {json_em}, Password: "
                                                          f"{json_pass}")
            else:
                messagebox.showinfo(title="Error", message="The data you are looking for does not exist!")
    else:
        messagebox.showinfo(title="Error", message="No data to search for!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.minsize(200, 200)
window.config(padx=40, pady=40)
window.title("Password Manager")
# canvas
logo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)
# labels of entries
website = Label(text="Website:", font=("Arial", 14))
website.grid(column=0, row=1)
email = Label(text="Email/Username:", font=("Arial", 14))
email.grid(column=0, row=2)
pw = Label(text="Password:", font=("Arial", 14))
pw.grid(column=0, row=3)
# entries
web_entry = Entry(width=18)
web_entry.grid(column=1, row=1)
web_entry.focus()
em_entry = Entry(width=35)
em_entry.grid(column=1, row=2, columnspan=2)
em_entry.insert(0, "kotadasarath@gmail.com")
pw_entry = Entry(width=18)
pw_entry.grid(column=1, row=3)
# buttons
search_button = Button(text="Search", width=13, command=search_password)
search_button.grid(column=2, row=1)
gen_pw = Button(text="Generate Password", command=generate_password)
gen_pw.grid(column=2, row=3)
add_button = Button(text="Add", width=35, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
