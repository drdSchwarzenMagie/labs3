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


def connect_with_ssh_tunnel():
    tunnel = SSHTunnelForwarder((ssh_host, ssh_port),
                                ssh_username=ssh_user,
                                ssh_password=ssh_password,
                                remote_bind_address=(db_server, db_port))
    tunnel.start()
    print("SSH туннель открыт на порту: ", tunnel.local_bind_port)
    connection_params = (
                "DRIVER={SQL Server};"
                f"SERVER=127.0.0.1,{tunnel.local_bind_port};"
                f"DATABASE={db_name};"
                f"UID={db_user};"
                f"PWD={db_password};"
                )
    connection = pyodbc.connect(connection_params)
    cursor = connection.cursor()

    return connection, cursor


connection, cursor = connect_with_ssh_tunnel()


def db_query(query: str, cursor=cursor):
    try:
        cursor.execute(query)
        if query.startswith("SELECT"):
            rows = cursor.fetchall()
            return rows
        elif query.split()[0] in ["DELETE", "UPDATE", "INSERT"]:
            cursor.commit()
            return True

    except pyodbc.Error as e:
        print(f"Query error: {e}")
        return False


def db_connection_close(connection=connection, cursor=cursor):
    cursor.close()
    connection.close()