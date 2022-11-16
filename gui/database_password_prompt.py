import tkinter as tk
from tkinter import Frame, Label, Entry, StringVar

import database
import global_values

fields = ['user', 'password', 'host', 'database']


class PasswordPrompt(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry(f"{300}x{200}")
        self.title("Database Information")
        self.frame = Frame(self)

        self.labels = []
        self.entries = []
        self.string_values = {}

        for i, field in enumerate(fields):
            self.string_values[field] = StringVar()
            self.labels.append(Label(self.frame, text=f"Enter {field} ".replace('database', 'database name')))
            self.labels[-1].pack(side="top", anchor="center")
            self.entries.append(Entry(self.frame, text=field))
            self.entries[-1].pack(side="top", anchor="center")
            if 'password' in field:
                self.entries[-1].configure(show='*')

        self.button = tk.Button(self.frame, text="Connect", command=self.connect)
        self.button.pack(side="top", anchor="center")

        self.frame.pack()

    def connect(self):
        for i, field in enumerate(fields):
            if len(self.entries[i].get()):
                global_values.global_values[field] = self.entries[i].get()
        try:
            database.connect(**global_values.global_values)
        except Exception as e:
            self.destroy()
            raise e

        self.destroy()
