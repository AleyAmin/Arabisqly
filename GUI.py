import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Window
from Connect_Database import *

cursor, conn = connect_to_database(DRIVER, SERVER, DATABASE)

class LoginPage:
    def __init__(self):
        self.id_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.content = ttk.Frame(main_window)
        self.Job = None
        self.create_widgets()

    def create_widgets(self):
        self.id_label = tk.Label(self.content, text="Id:")
        self.id_label.pack(pady=5)
        self.id_entry = tk.Entry(self.content, textvariable=self.id_var)
        self.id_entry.pack(pady=5)

        self.password_label = tk.Label(self.content, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.content, textvariable=self.password_var, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.content, text="Login", command=self.login)
        self.login_button.pack(pady=5)

    def login(self):
        id = self.id_var.get()
        password = self.password_entry.get()

        try:
            cursor.execute("EXEC Login_func ?, ?", (id, password))
            row = cursor.fetchall()
            if len(row) == 1:
                self.Job = row[0][1]
                messagebox.showinfo("Login Successful", "Welcome, Admin!\nJob: " + self.Job)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def show_frame(self):
        self.content.pack(fill="both", expand=True)

    def hide_frame(self):
        self.content.pack_forget()

main_window = Window(themename='darkly')
main_window.geometry("800x600")
main_window.title("Arabisqly")
login_page = LoginPage()

