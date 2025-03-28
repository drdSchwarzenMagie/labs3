import pyodbc
from sshtunnel import SSHTunnelForwarder

ssh_host = 'kappa.cs.petrsu.ru'
ssh_port = 22
ssh_user = 'umfedoto'       # Имя пользователя для SSH
ssh_password = 'aeRiel4s'  # Пароль для SSH (или используйте ключ)

db_server = '192.168.112.103'
db_port = 1433
db_name = 'db22207'
db_user = 'User095'              # Логин для базы данных
db_password = 'User095{*27'      # Пароль для базы данных



def db_select(query):
    try:
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(db_server, db_port)
        ) as tunnel:
            print(f"SSH-туннель открыт на локальном порту: {tunnel.local_bind_port}")

            connection_string = (
                "DRIVER={SQL Server};"
                f"SERVER=127.0.0.1,{tunnel.local_bind_port};"
                f"DATABASE={db_name};"
                f"UID={db_user};"
                f"PWD={db_password};"
            )

            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute(query)

            rows = cursor.fetchall()
            for row in rows:
                print(row)

            return rows

    except Exception as e:
        print("Ошибка:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def db_change_data(query):
    try:
        with SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_server, db_port)
        ) as tunnel:
            print(f"SSH-туннель открыт на локальном порту: {tunnel.local_bind_port}")

            connection_string = (
                "DRIVER={SQL Server};"
                f"SERVER=127.0.0.1,{tunnel.local_bind_port};"
                f"DATABASE={db_name};"
                f"UID={db_user};"
                f"PWD={db_password};"
            )

            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute(query)
            cursor.commit()

            return True

    except Exception as e:
        print("Ошибка:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


db_select('SELECT * FROM "tblFlat"')