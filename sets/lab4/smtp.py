from socket import *

msg = ("From: umfedoto@cs.karelia.ru\r\n"
       "To: umfedoto@cs.karelia.ru\r\n"
       "Subject: Тестовое письмо\r\n"
       "Content-Type: text/plain; charset=utf-8\r\n"
       "\r\n"
       "Я люблю компьютерные сети!")

endmsg = "\r\n.\r\n"

# Выбираем почтовый сервер и порт
mailserver = ("mx2.sampo.ru", 25)  # Адрес сервера и порт SMTP (обычно 25)

# Создаем сокет clientSocket и устанавливаем TCP-соединение
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('Код 220 от сервера не получен.')

# Отправляем команду HELO
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('Код 250 от сервера не получен.')

# Отправляем команду MAIL FROM
mailFrom = 'MAIL FROM:<umfedoto@cs.karelia.ru>\r\n'
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)

# Отправляем команду RCPT TO
rcptTo = 'RCPT TO:<umfedoto@cs.karelia.ru>\r\n'
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)

# Отправляем команду DATA
data = 'DATA\r\n'
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)

# Отправляем текст сообщения
clientSocket.send(msg.encode())

# Завершаем сообщение точкой
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)

# Отправляем команду QUIT
quit = 'QUIT\r\n'
clientSocket.send(quit.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)

# Закрываем соединение
clientSocket.close()
