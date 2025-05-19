import sys
from PySide6.QtWidgets import QApplication

# Подключение к БД через SSH
from db_connection import connect_with_ssh_tunnel, db_connection_close
from main_menu_window import MainMenuWindow


def main():
    connection, cursor = connect_with_ssh_tunnel()

    app = QApplication(sys.argv)
    

    menu_window = MainMenuWindow(cursor, connection)
    menu_window.show()

    exit_code = app.exec()
    db_connection_close(connection, cursor)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()