<?php
header("Content-Type: text/html; charset=utf-8");

// Имя XML-файла с тестом
$xml_file = "test_xml";

// Проверка существования файла
if (!file_exists($xml_file)) {
    die("Файл теста не найден.");
}

// Загрузка и обработка XML
$xml_content = file_get_contents($xml_file);
$xml_content = preg_replace('/\s+/', ' ', $xml_content); // Удаляем повторяющиеся пробелы
$xml = simplexml_load_string($xml_content);
if ($xml === false) {
    die("Ошибка загрузки XML.");
}

// Функция обработки строки: удаление пробелов, приведение первого символа к верхнему регистру, экранирование спецсимволов
function clean_text($text) {
    $text = trim($text);
    $text = ucfirst($text);
    return htmlspecialchars($text, ENT_QUOTES, 'UTF-8');
}

// Вывод теста
echo "<ul style='max-width: 600px; word-wrap: break-word;'>";
foreach ($xml->question as $question) {
    $q_id = (int)$question['id'];
    $q_name = clean_text($question->name);
    
    echo "<li><strong>$q_id. $q_name</strong></li>";
    echo "<ul>";

    foreach ($question->answer as $answer) {
        $a_id = (int)$answer['id'];
        $a_text = clean_text($answer);
        echo "<li>$q_id.$a_id $a_text</li>";
    }

    echo "</ul>";
}
echo "</ul>";
?>
