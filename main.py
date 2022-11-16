import argparse
from threading import Thread

import database
from gui.database_password_prompt import PasswordPrompt
from global_values import global_values
from monitor import Monitor

version = '1.0.0'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', type=str, default=0)
    parser.add_argument('-p', '--password', type=str, default=0)
    parser.add_argument('-i', '--ip', type=str, default=0)
    parser.add_argument('-d', '--database', type=str, default=0)
    args = parser.parse_args()
    if args.user:
        database.connect(user=args.user, password=args.password, host=args.ip, database=args.database)
    else:
        password_prompt = PasswordPrompt()
        password_prompt.mainloop()

    db_params = global_values

    monitor = Monitor(2)
    while True:
        pass
