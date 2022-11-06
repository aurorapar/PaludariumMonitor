from uuid import uuid4

import mysql.connector as db

table_name = 'monitored_info'
desired_values = ['time_stamp', 'humidity', 'temperature', 'water']


def connect(**database_values):
    return db.connect(**database_values)


fetch_query = "SELECT "
for column in desired_values:
    fetch_query += column
    if column != desired_values[-1]:
        fetch_query += ","
    fetch_query += " "
fetch_graph_value_query = (f"""{fetch_query} FROM {table_name}""")

print(fetch_graph_value_query)

insert_monitored_data = (
                        "INSERT INTO "
                        "monitored_info (uuid, time_stamp, humidity, temperature, water) "
                        "VALUES ('" + str(uuid4()) + "', %s, %s, %s, %s)"
                        )
