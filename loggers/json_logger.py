import json
import os
import sys

from datetime import datetime
from enum import auto
from traceback import format_exception
from uuid import uuid4

# TODO: this is a hacky solution for imports. Consider revision.
sys.path.append(os.getcwd())

TIME_FORMAT = '%C%Y-%m-%d_%H-%M-%S'

logging_dir = os.path.join(os.getcwd(), 'graph_data')
log_file = os.path.join(logging_dir, 'json_log.json')


class JsonLogger:

    def __init__(self):
        JsonLogger.create_log()

    @staticmethod
    def add_log_item(message, exception=None):

        message = LogData(message)

        log = None
        try:
            with open(log_file, 'r') as f:
                log = json.load(f)
        except json.decoder.JSONDecodeError:
            if os.path.getsize(log_file):
                os.remove(log_file)
            else:
                print("Log file corrupted, moving and creating new file")
                os.rename(log_file, os.path.join(logging_dir, ('corrupted_' + os.path.basename(log_file))))
            JsonLogger.create_log()
            JsonLogger.add_log_item(message.content)
            return

        with open(log_file, 'w') as f:
            log.append((message.uuid, message.date, message.content))
            json.dump(log, f, indent=4)

    @staticmethod
    def create_log():
        if not os.path.exists(logging_dir):
            os.mkdir(logging_dir)

        if not os.path.exists(log_file):

            with open(log_file, 'w') as f:
                json.dump([], f, indent=4)


class LogData:

    def __init__(self, data):

        self.uuid = str(uuid4())
        self.date = datetime.strftime(datetime.now(), TIME_FORMAT)
        self.content = data

    def __str__(self):
        return f"{self.uuid} created at {self.date}\n{self.content}"


json_logger = JsonLogger()


if __name__ == '__main__':
    JsonLogger.add_log_item(("Humidity", 10))
