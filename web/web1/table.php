<?php

// Определение всех переменных внутри текущего скрипта
$a      = 15;        # целое
$fl     = 3.14;      # с плавающей точкой
$boo    = TRUE;      # boolean
$str    = "stroka";  # строка
$nol    = 0;
$pusto  = "";

$s1 = "Переменная a = $a \n";   # разбираемая строка
$s2 = 'Переменная a = $a \n';   # неразбираемая строка

$mas = array( "one" => TRUE,
        1   => -20,
          "three" => 3.14);
$mas[]="two";
$mas["four"]=4;

// Создание таблицы
echo '<html><head><style>
    table {width: 100%; border-collapse: collapse;}
    th, td {border: 1px solid black; padding: 8px; text-align: center;}
    th {background-color: #f2f2f2;}
    </style></head><body>';
echo '<table>';

// Заголовок таблицы
echo '<tr><th>Номер задания</th><th>Решение</th><th>Результат</th></tr>';

// Задание 1: Вывести значение переменных $a, $fl, $boo, $str
echo '<tr><td>1</td><td>echo "$a, $fl, $boo, $str";</td><td>';
echo "$a, $fl, $boo, $str";
echo '</td></tr>';

// Задание 2: Вывести результат сложения переменных $a и $str
echo '<tr><td>2</td><td>echo $a + $str;</td><td>';
try {
    // Пытаемся сложить переменные
    if (!is_numeric($str)) {
        throw new Exception("Невозможно сложить число и строку");
    }
    echo $a + $str;
} catch (Exception $e) {
    // Обработка исключения
    echo "Ошибка: " . $e->getMessage(); // Выводим ошибку
}
echo '</td></tr>';

// Задание 3: Вывести результат сравнения переменных $a и $str
echo '<tr><td>3</td><td>echo $a == $str;</td><td>';
echo $a == $str ? 'true' : 'false'; // Сравнение с приведением типов
echo '</td></tr>';

// Задание 4: Вывести результат сравнения переменных $nol и $pusto с использованием операторов == и ===
echo '<tr><td>4</td><td>echo $nol == $pusto, " и ", $nol === $pusto;</td><td>';
echo $nol == $pusto ? 'true' : 'false';
echo ' и ';
echo $nol === $pusto ? 'true' : 'false'; // Сравнение с учетом типов
echo '</td></tr>';

// Задание 5: Сравнить результат вывода переменных $s1 и $s2
echo '<tr><td>5</td><td>echo $s1 == $s2;</td><td>';
echo $s1 == $s2 ? 'true' : 'false'; // Сравнение с приведением типов
echo '</td></tr>';

// Задание 6: Вывести $mas["one"], $mas[2], $mas[3]
echo '<tr><td>6</td><td>echo $mas["one"], $mas[2], $mas[3];</td><td>';
echo $mas["one"], ', ';
// Проверяем существование индекса перед выводом
if (isset($mas[2])) {
    echo $mas[2], ', ';
} else {
    echo ', ', '';
}

// Проверяем существование индекса 3 перед выводом
if (isset($mas[3])) {
    echo $mas[3];
} else {
    echo '';
}
echo '</td></tr>';

// Задание 7: С помощью var_dump() вывести массив $mas
echo '<tr><td>7</td><td>var_dump($mas);</td><td>';
var_dump($mas);
echo '</td></tr>';

// Задание 8: Вывести преобразование в строку (string)$fl (или strval($fl)) значения переменной $fl
echo '<tr><td>8</td><td>echo (string)$fl;</td><td>';
echo (string)$fl; // или strval($fl)
echo '</td></tr>';

// Задание 9: Вывести преобразование в строку массива $mas
echo '<tr><td>9</td><td>echo (string)$mas;</td><td>';
// Используем print_r() для корректного отображения массива как строки
echo '<pre>';
print_r($mas);  // Отображение массива в виде строки
echo '</pre>';
echo '</td></tr>';


// Задание 10: Вывести значение переменной $a, используя синтаксис "переменные переменных"
echo '<tr><td>10</td><td>echo ${$name};</td><td>';
$name = "a";  // Переменная переменных
echo ${$name}; // Вывод значения переменной $a
echo '</td></tr>';

// Закрытие таблицы
echo '</table></body></html>';
?>
