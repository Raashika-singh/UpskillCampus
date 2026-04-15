import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import string

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT,
    username TEXT,
    password TEXT
)
""")

conn.commit()

# ---------------- FUNCTIONS ---------------- #

def generate_password():
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%&*"

    password = (
        random.choice(letters) +
        random.choice(digits) +
        random.choice(symbols) +
        ''.join(random.choice(letters + digits + symbols) for _ in range(8))
    )

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website == "" or username == "" or password == "":
        messagebox.showwarning("Error", "Please fill all fields")
        return

    cursor.execute(
        "INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
        (website, username, password)
    )
    conn.commit()

    messagebox.showinfo("Success", "Password saved successfully")

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def search_password():
    website = website_entry.get()

    cursor.execute(
        "SELECT username, password FROM passwords WHERE website=?",
        (website,)
    )

    result = cursor.fetchone()

    if result:
        username, password = result
        messagebox.showinfo(
            "Details",
            f"Username: {username}\nPassword: {password}"
        )
    else:
        messagebox.showerror("Not Found", "No data found for this website")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Password Manager")
root.geometry("400x300")

tk.Label(root, text="Website").pack(pady=5)
website_entry = tk.Entry(root, width=35)
website_entry.pack()

tk.Label(root, text="Username / Email").pack(pady=5)
username_entry = tk.Entry(root, width=35)
username_entry.pack()

tk.Label(root, text="Password").pack(pady=5)
password_entry = tk.Entry(root, width=35)
password_entry.pack()

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=5)

tk.Button(root, text="Save Password", command=save_password).pack(pady=5)

tk.Button(root, text="Search Password", command=search_password).pack(pady=5)

root.mainloop()

conn.close()