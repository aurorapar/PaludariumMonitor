import time
import tkinter as tk
from tkinter import Label, Entry, Frame, Button, RAISED

import matplotlib.pyplot as plt

from database import fetch_graph_value_query, insert_monitored_data
from plotter import Graph

monitored_values = ['Humidity %', 'Temp C°', 'Water Level cm']

window_width = 300
window_height = 250
window_size = f"{window_width}x{window_height}"

column_start = 2
row_start = 3

pad_x = 10
pad_y = 10


class Root(tk.Tk):

    def __init__(self, db_connection):
        super().__init__()
        self.title("Paludarium Monitor")
        self.resizable(width=False, height=False)
        self.geometry(window_size)

        self.widgets = {'labels': [], 'entries': [], 'buttons': []}

        self.frame = Frame(self, width=window_width-10, height=window_height-10)
        self.frame.grid(row=0, column=1, columnspan=10)

        for i, value_name in enumerate(monitored_values):
            label_row = (i+1) * row_start
            label_column = column_start
            entry_row = label_row + 1
            entry_column = label_column

            label = Label(self.frame, text=value_name, padx=pad_x, pady=pad_y)
            self.widgets['labels'].append(label)
            label.grid(row=label_row, column=label_column)

            entry = Entry(self.frame, width=4)
            self.widgets['entries'].append(entry)
            entry.grid(row=entry_row, column=entry_column)

        submit_row = len(self.widgets['labels']) * 2 + 1
        submit_column = 4
        submit_button = Button(self.frame, text="Submit Values", command=self.submit_values, relief=RAISED)
        self.widgets['buttons'].append(submit_button)
        submit_button.grid(row=submit_row, column=submit_column)

        graph_row = len(self.widgets['labels']) * 3 + 2
        graph_column = column_start + 2
        graph_button = Button(self.frame, text="Graph", command=self.build_graph, relief=RAISED)
        self.widgets['buttons'].append(graph_button)
        graph_button.grid(row=graph_row, column=graph_column)

        self.graph = None

        if not db_connection:
            self.destroy()
        self.db_connection = db_connection
        self.cursor = self.db_connection.cursor()

    def submit_values(self):
        value_entries = tuple(float(entry.get()) for entry in self.widgets['entries'])
        value_entries = (int(time.time()),) + value_entries
        print(value_entries)
        try:
            self.cursor.execute(insert_monitored_data, value_entries)
            self.db_connection.commit()
            print("Successful Commit")
        except Exception as e:
            self.db_connection.rollback()
            print("Rolled back")
            print(e)

        self.build_graph()

    def build_graph(self):
        self.cursor.execute(fetch_graph_value_query)
        data_returned = self.cursor.fetchall()
        sorted_data = []
        for data_set_number in range(len(data_returned[0])):
            sorted_data.append([n[data_set_number] for n in data_returned])

        if not self.graph:
            self.graph = Graph("Paludarium Values", "Time (days)", ([],), monitored_values, ([], [], []),
                               colors=("paleturquoise", "firebrick", "deepskyblue"))

        self.graph.update(sorted_data[0], (sorted_data[1:]))
