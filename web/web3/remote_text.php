<?php
session_start();

// Проверка аутентификации
if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true) {
    header('Location: login.php');
    exit();
}

// Получение и вывод содержимого удаленного файла
$url = 'http://kappa.cs.petrsu.ru/~kulakov/courses/php/fortune.php';
$content = file_get_contents($url);

// Выводим содержимое как HTML
echo $content;
?>
