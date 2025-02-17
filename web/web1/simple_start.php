<?php

/* Описание скалярных переменных */

$a      = 15;        # целое
$fl     = 3.14;         # с плавающей точкой
$boo     = TRUE;         # boolean
$str    = "string";     # строка
$nol    = 0;
$pusto    = "";
$name = "a";
$s1 = "Переменная a = $a \n";   # разбираемая строка
$s2 = 'Переменная a = $a \n';   # неразбираемая строка

$file_list = `ls -a`;
/* Описание массива */

$mas = array( "one" => TRUE,
        1   => -20,
          "three" => 3.14);
$mas[]="two";
$mas["four"]=4;

$mas_add = [
  "five" => 5,
  6 => "six",
  "seven" => 7.77
];

$merged_mas = $mas + $mas_add;

for ($i = 1; $i <= 3; $i++) {
  ${"var".$i} = 0;
}
/* Описание константы */

define("HOST", "kappa.cs.karelia.ru");

$str1 = $HOST;
$str2 = @$HOST;

?>