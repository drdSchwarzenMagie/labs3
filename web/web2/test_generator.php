<?php
// test_generator.php
header("Content-Type: text/html; charset=UTF-8");

// Читаем файл с тестом
$filename = "test_xml";
if (!file_exists($filename)) {
    die("Файл с тестом не найден.");
}

$xmlContent = file_get_contents($filename);

// Удаляем XML-декларацию
$xmlContent = preg_replace('/<\?xml.*?\?>/', '', $xmlContent);

// Убираем теги <test>
$xmlContent = preg_replace('/<\/?test\s*>/', '', $xmlContent);

// Приводим теги к нормальному виду
$xmlContent = preg_replace('/<\s*(\/?\w+)\s*>/u', '<$1>', $xmlContent);
$xmlContent = preg_replace('/<\s*(\w+)\s+([^>]+)>/u', '<$1 $2>', $xmlContent);
$xmlContent = preg_replace('/<\/\s*(\w+)\s*>/u', '</$1>', $xmlContent);

// Разбиваем на строки
$lines = preg_split('/\r?\n/', $xmlContent);
$questions = [];
$currentQuestion = null;

foreach ($lines as $line) {
    // Удаляем пробелы в начале/конце строки и лишние пробелы между словами
    $line = trim(preg_replace('/\s+/', ' ', $line));
    if (empty($line)) continue;

    // Парсим вопрос
    if (preg_match('/<question/', $line)) {
        $currentQuestion = ['name' => '', 'answers' => []];
    } elseif (preg_match('/<name>(.*?)<\/name>/', $line, $matches)) {
        $text = trim($matches[1]);
        $text = html_entity_decode($text, ENT_QUOTES, "UTF-8"); // Декодируем спецсимволы
        $text = mb_strtoupper(mb_substr($text, 0, 1, "UTF-8"), "UTF-8") . mb_substr($text, 1, null, "UTF-8");
        $text = htmlspecialchars($text, ENT_QUOTES, "UTF-8"); // Обратно кодируем спецсимволы
        $currentQuestion['name'] = $text;
    } elseif (preg_match('/<answer[^>]*>(.*?)<\/answer>/', $line, $matches)) {
        $text = trim($matches[1]);
        $text = html_entity_decode($text, ENT_QUOTES, "UTF-8"); // Декодируем спецсимволы
        $text = mb_strtoupper(mb_substr($text, 0, 1, "UTF-8"), "UTF-8") . mb_substr($text, 1, null, "UTF-8");
        $text = htmlspecialchars($text, ENT_QUOTES, "UTF-8"); // Обратно кодируем спецсимволы
        $currentQuestion['answers'][] = $text;
    } elseif (preg_match('/<\/question>/', $line)) {
        $questions[] = $currentQuestion;
    }
}

// Вывод HTML
echo "<!DOCTYPE html>\n<html lang='ru'>\n<head>\n<meta charset='UTF-8'>\n";
echo "<title>Тест</title>\n<style>body { font-family: Arial, sans-serif; max-width: 600px; word-wrap: break-word; }</style>\n</head>\n<body>\n";
echo "<h2>Тест</h2>\n<ol>\n";

foreach ($questions as $qIndex => $question) {
    echo "<li>{$question['name']}\n<ul>\n";
    foreach ($question['answers'] as $aIndex => $answer) {
        echo "<li>" . ($qIndex + 1) . "." . ($aIndex + 1) . " $answer</li>\n";
    }
    echo "</ul>\n</li>\n";
}

echo "</ol>\n</body>\n</html>";
?>
