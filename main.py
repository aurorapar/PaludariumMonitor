version = '1.0.0'

from database import connect
from gui.root import Root
from gui.database_password_prompt import PasswordPrompt
import global_values

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    password_prompt = PasswordPrompt()
    password_prompt.mainloop()

    db_params = global_values.global_values
    db_connection = connect(**db_params)

    gui_root = Root(db_connection)
    gui_root.mainloop()

