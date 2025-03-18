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

    // Кодируем тему в UTF-8
    $subject = "=?UTF-8?B?" . base64_encode($subject) . "?=";

    // Формируем заголовки
    $headers = "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $headers .= "Content-Transfer-Encoding: 8bit\r\n";
    $headers .= "From: <$from>\r\n";
    $headers .= "To: <$to>\r\n";
    $headers .= "Subject: $subject\r\n\r\n";

    // Отправка заголовков и тела письма
    fwrite($socket, $headers . $message . "\r\n.\r\n");
    echo fgets($socket, 512);

    // Завершение сессии
    fwrite($socket, "QUIT\r\n");
    echo fgets($socket, 512);

    fclose($socket);
}

// Вызов функции отправки почты
sendSmtpMail($host, $port, $to, $from, $subject, $message);
?>
