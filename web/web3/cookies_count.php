<?php
session_start();

if (isset($_COOKIE['visits'])) {
    $visits = $_COOKIE['visits'] + 1;
} else {
    $visits = 1;
}

setcookie('visits', $visits, time() + (30 * 24 * 60 * 60));

if ($visits == 1) {
    echo "Добро пожаловать!";
} else {
    echo "Вы посетили эту страницу $visits раз";
}
?>