import socket
import ssl
import base64

# Настройки
smtp_server = 'smtp.gmail.com'
port = 587
username = 'fedula22012111@gmail.com'
password = 'your_app_password'  # Важно: используйте пароль приложения (а не обычный пароль Google)

# Сообщение
from_addr = username
to_addr = username
subject = "Тест TLS"
body = "Я люблю компьютерные сети!"

# Создание TCP-соединения
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((smtp_server, port))
recv = clientSocket.recv(1024).decode()
print(recv)

# Команда EHLO
clientSocket.send(b'EHLO test\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

# Запуск TLS
clientSocket.send(b'STARTTLS\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

# Обертывание SSL
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=smtp_server)

# Повторная команда EHLO после TLS
clientSocket.send(b'EHLO test\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

# Аутентификация
clientSocket.send(b'AUTH LOGIN\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

# Логин и пароль (в base64)
clientSocket.send(base64.b64encode(username.encode()) + b'\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

# MAIL FROM
clientSocket.send(f'MAIL FROM:<{from_addr}>\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# RCPT TO
clientSocket.send(f'RCPT TO:<{to_addr}>\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)

# DATA
clientSocket.send(b'DATA\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

# Сообщение с заголовками
headers = (f"From: {from_addr}\r\n"
           f"To: {to_addr}\r\n"
           f"Subject: {subject}\r\n"
           "Content-Type: text/plain; charset=utf-8\r\n"
           "\r\n")
clientSocket.send(headers.encode('utf-8') + body.encode('utf-8') + b'\r\n.\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

# QUIT
clientSocket.send(b'QUIT\r\n')
recv = clientSocket.recv(1024).decode()
print(recv)

clientSocket.close()
