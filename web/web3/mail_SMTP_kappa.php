<?php
// SMTP параметры
$host = 'mail.cs.karelia.ru';
$port = 25;
$to = 'umfedoto@cs.karelia.ru';
$from = 'fedula22012111@gmail.com';
$subject = 'Тестовое сообщение';
$message = 'Это тестовое сообщение отправлено с помощью PHP.';

// Функция для отправки SMTP-запроса
function sendSmtpMail($host, $port, $to, $from, $subject, $message) {
    $socket = fsockopen($host, $port);
    if (!$socket) {
        die('Не удалось подключиться к SMTP серверу');
    }

    // Отправка команды HELO
    fwrite($socket, "HELO $host\r\n");
    echo fgets($socket, 512);

    // Установка отправителя
    fwrite($socket, "MAIL FROM: <$from>\r\n");
    echo fgets($socket, 512);

    // Установка получателя
    fwrite($socket, "RCPT TO: <$to>\r\n");
    echo fgets($socket, 512);

    // Начало передачи данных
    fwrite($socket, "DATA\r\n");
    echo fgets($socket, 512);

    // Отправка сообщения
    fwrite($socket, "Subject: $subject\r\n\r\n$message\r\n.\r\n");
    echo fgets($socket, 512);

    // Завершение сессии
    fwrite($socket, "QUIT\r\n");
    echo fgets($socket, 512);

    fclose($socket);
}

// Вызов функции отправки почты
sendSmtpMail($host, $port, $to, $from, $subject, $message);
?>