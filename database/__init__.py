import time

import mysql.connector as db

cnx = None
cursor = None

database_name = 'paludarium_monitor'
table_name = 'monitored_info'

desired_values = ['time_stamp', 'humidity', 'temperature']

create_tables_query = f"""
CREATE TABLE IF NOT EXISTS {database_name}.{table_name} (
    id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    time_stamp BIGINT UNSIGNED,
    last_modified BIGINT UNSIGNED,
    humidity DECIMAL(3,1),
    temperature DECIMAL(3,1)
    )
"""

fetch_query = "SELECT "
for column in desired_values:
    fetch_query += column
    if column != desired_values[-1]:
        fetch_query += ","
    fetch_query += " "
fetch_graph_value_query = (f"""{fetch_query} FROM {table_name}""")

insert_monitored_data = (
                        "INSERT INTO "
                        "monitored_info (time_stamp, humidity, temperature, last_modified) "
                        "VALUES (%s, %s, %s, %s)"
                        )


def connect(**database_values):
    global cnx, cursor, database_name
    database_name = database_values['database']
    cnx = db.connect(**database_values)
    cursor = cnx.cursor()
    create_database()


def create_database(**database_values):
    cursor.execute(create_tables_query)


def update_database(conditions):
    values = []
    for key in conditions.keys():
        if key not in desired_values:
            raise ValueError(f"{key} is not a loggable value")
    for field in desired_values[1:]:
        values.append(conditions[field])
    values = (int(time.time()),) + tuple(values) + (int(time.time()),)
    cursor.execute(insert_monitored_data, values)
    cnx.commit()


def get_start_date():
    cursor.execute(f"SELECT MIN(time_stamp) FROM {table_name}")
    return cursor.fetchone()[0]


def get_end_date():
    cursor.execute(f"SELECT MAX(time_stamp) FROM {table_name}")
    return cursor.fetchone()[0]


def get(item):
    if item not in desired_values:
        raise ValueError(f"Can't get {item} from database, column doesn't exist")
    cursor.execute(f"SELECT {item} FROM {table_name} ORDER BY id")
    return cursor.fetchall()


if __name__ == "__main__":
    print(create_tables_query)
    print(insert_monitored_data)