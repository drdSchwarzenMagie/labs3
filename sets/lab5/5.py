# Импортируем модуль для работы с сокетами
from socket import *

# Создаем сокет сервера
serverSocket = socket(AF_INET, SOCK_STREAM)

# Подготавливаем сокет сервера
# Начало вставки
serverSocket.bind(('', 6789))  # Привязываем сокет к порту 6789
serverSocket.listen(1)         # Переходим в режим прослушивания
# Конец вставки

while True:
    # Устанавливаем соединение
    print('Готов к обслуживанию...')
    connectionSocket, addr = serverSocket.accept()  # Принимаем входящее соединение

    try:
        # Получаем HTTP-запрос от клиента
        message = connectionSocket.recv(1024).decode()  # Читаем данные из сокета
        filename = message.split()[1]  # Извлекаем имя файла из запроса
        f = open(filename[1:])  # Открываем файл (убираем первый символ '/')
        outputdata = f.read()  # Читаем содержимое файла

        # Отправляем в сокет одну строку HTTP-заголовка
        # Начало вставки
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())  # Статус успешного ответа
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())  # Тип контента
        # Конец вставки

        # Отправляем содержимое запрошенного файла клиенту
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()

    except IOError:
        # Отправляем ответ об отсутствии файла на сервере
        # Начало вставки
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())  # Статус ошибки
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())  # Тип контента
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())  # Сообщение об ошибке
        # Конец вставки

        # Закрываем клиентский сокет
        # Начало вставки
        connectionSocket.close()
        # Конец вставки

# Закрываем серверный сокет (этот код никогда не выполнится, так как сервер работает в бесконечном цикле)
serverSocket.close()