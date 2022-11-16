import time
from threading import Thread

import board

import database

from global_values import TIME_FORMAT
from modules.dht22 import DHT22
from plotter import Graph


def get_paludarium_conditions():
    sensor = DHT22(board.D27)
    return {'temperature': sensor.get_temperature(),
            'humidity': sensor.get_humidity()}


class Monitor:

    def __init__(self, loop_time):
        start_date = time.localtime(database.get_start_date()) or time.strftime(TIME_FORMAT)
        end_date = time.localtime(database.get_end_date()) or time.strftime(TIME_FORMAT)
        self.graph = Graph(
            f"Paludarium Monitor\n{time.strftime(TIME_FORMAT, start_date)} - {time.strftime(TIME_FORMAT, end_date)}",
            "Time (h)", ([],), ('Temperature', 'Humidity'), ([], []), colors=('firebrick', 'paleturquoise'))

        self.thread = Thread(target=self.run, args=(loop_time,))
        self.thread.setDaemon(True)
        self.thread.start()

        conditions_thread = Thread(target=self.update_conditions)
        conditions_thread.setDaemon(True)
        conditions_thread.start()

    def run(self, loop_time):
        while True:
            start_time = time.perf_counter()
            times = database.get('time_stamp')
            temps = database.get('temperature')
            humids = database.get('humidity')
            end_time = time.perf_counter()
            print(f"Took {end_time - start_time}s to query db")
            self.graph.update(times, (temps, humids))
            end_time = time.perf_counter()
            print(f"Took {end_time-start_time}s to do main loop")
            time.sleep(loop_time)

    def update_conditions(self):
        while True:
            start_time = time.perf_counter()
            try:
                conditions = get_paludarium_conditions()
            except RuntimeError:
                continue
            database.update_database(conditions)
            end_time = time.perf_counter()
            print(f"Took {end_time - start_time}s to do tertiary loop")
            time.sleep(2.1)
