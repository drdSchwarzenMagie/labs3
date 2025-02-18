<?php
// Подключаем файл simple_start.php
include 'simple_start.php';

// Массив с заданиями
$tasks = [
    [
        'number' => 1,
        'solution' => 'echo $a; echo $fl; echo $boo; echo $str;',
        'result' => $a . ' ' . $fl . ' ' . ($boo ? 'TRUE' : 'FALSE') . ' ' . $str
    ],
    [
        'number' => 2,
        'solution' => 'echo $a + $str;',
        'result' => "Fatal error: Uncaught TypeError: Unsupported operand types: int + string"
    ],
    [
        'number' => 3,
        'solution' => 'echo $a == $str;',
        'result' => ($a == $str) ? 'TRUE' : 'FALSE'
    ],
    [
        'number' => 4,
        'solution' => 'echo $nol == $pusto; echo $nol === $pusto;',
        'result' => ($nol == $pusto ? 'TRUE' : 'FALSE') . ' ' . ($nol === $pusto ? 'TRUE' : 'FALSE')
    ],
    [
        'number' => 5,
        'solution' => 'echo $s1; echo $s2;',
        'result' => $s1 . $s2 
    ],
    [
        'number' => 6,
        'solution' => '$mas["one"], $mas[2], $mas[3]',
        'result' => "{$mas['one']}, {$mas[2]}, {$mas[3]}"
    ],
    [
        'number' => 7,
        'solution' => 'var_dump($mas)',
        'result' => ''
    ],
    [
        'number' => 8,
        'solution' => '(string)$fl',
        'result' => (string)$fl
    ],
    [
        'number' => 9,
        'solution' => 'print_r($mas, true)',
        'result' => print_r($mas, true)
    ],
    [
        'number' => 10,
        'solution' => '${$name}',
        'result' => ${$name}
    ],
    [
        'number' => 11,
        'solution' => '$var1, $var2, $var3',
        'result' => "$var1, $var2, $var3"
    ],
    [
        'number' => 12,
        'solution' => '$ref = & $a; $ref = 20;',
        'result' => 
            (function() {
                global $a;
                $ref = &$a; 
                $ref = 20;  
                return $a;  
            })()
    ],
    [
        'number' => 13,
        'solution' => 'HOST',
        'result' => HOST
    ],
    [
        'number' => 14,
        'solution' => '$str=$HOST; $str=@$HOST;',
        'result' => "$str1; $str2"
    ],
    [
        'number' => 15,
        'solution' => '$file_list = `ls -a`; echo $file_list;',
        'result' => $file_list
    ],
    [
        'number' => 16,
        'solution' => '$str.$nol . 1',
        'result' => ($str . $nol . '1')
    ],
    [
        'number' => 17,
        'solution' => '$merged_mas = $mas + $mas_add; var_dump($merged_mas)',
        'result' => ''
    ]
];
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сводная таблица решений заданий</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            border: 1px solid black;
            text-align: left;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 0;
        }
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
    </style>
</head>
<body>
    <h1>Сводная таблица решений заданий</h1>
    <table>
        <thead>
            <tr>
                <th>Номер задания</th>
                <th>Решение</th>
                <th>Результат</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($tasks as $task): ?>
                <tr>
                    <td><?php echo $task['number']; ?></td>
                    <td><pre><?php echo $task['solution']; ?></pre></td>
                    <td><pre><?php 
                    if ($task['number'] == 7) {
                        var_dump($mas); 
                    }
                    if ($task['number'] == 17) {
                        var_dump($merged_mas); 
                    }
                    echo $task['result']; ?></pre></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</body>
</html>
