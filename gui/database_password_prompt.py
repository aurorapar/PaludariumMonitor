import tkinter as tk
from tkinter import Frame, Label, Entry, StringVar

import global_values

fields = ['user', 'password', 'host', 'database']
creds = {'user': 'aquarium_monitor', 'password': 'axolotl0421', 'host':'192.168.1.142',
         'database': 'paludarium_monitor'}


class PasswordPrompt(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry(f"{300}x{200}")
        self.frame = Frame(self)

        self.labels = []
        self.entries = []
        self.string_values = {}

        for i, field in enumerate(fields):
            self.string_values[field] = StringVar()
            self.labels.append(Label(self.frame, text=f"Enter {field} ".replace('database', 'database name')))
            self.labels[-1].pack(side="top", anchor="center")
            # self.labels[-1].place(anchor='center')  # grid(row=i*2, column=0)
            self.entries.append(Entry(self.frame, text=field))
            self.entries[-1].pack(side="top", anchor="center")
            # self.entries[-1].place(relx=0, rely=0, anchor='center')  # .grid(row=i*2 + 1, column=0)
            if 'password' in field:
                self.entries[-1].configure(show='*')

        self.button = tk.Button(self.frame, text="Connect", command=self.connect)
        self.button.pack(side="top", anchor="center")
        # self.button.place(relx=0, rely=0, anchor='center')  # grid(row=len(fields)*2+1, column=0)

        self.frame.pack()

    def connect(self):
        for i, field in enumerate(fields):
            if len(self.entries[i].get()):
                global_values.global_values[field] = self.entries[i].get()

        if not global_values.global_values.values():
            global_values.global_values = {key: value for key, value in creds.items()}

        self.destroy()
