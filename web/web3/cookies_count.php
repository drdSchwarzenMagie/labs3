<?php
session_start();

// Проверяем наличие cookie с количеством посещений
if (isset($_COOKIE['visits'])) {
    $visits = $_COOKIE['visits'] + 1;
} else {
    $visits = 1;
}

// Устанавливаем новое значение cookie на 30 дней
setcookie('visits', $visits, time() + (30 * 24 * 60 * 60));

if ($visits == 1) {
    echo "Добро пожаловать!";
} else {
    echo "Вы посетили эту страницу $visits раз";
}
?>