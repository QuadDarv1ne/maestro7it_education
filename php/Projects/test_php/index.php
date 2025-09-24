<?php
// Создание массива
$fruits = array("Яблоко", "Апельсин", "Банан");

// Добавление элементов
array_push($fruits, "Виноград", "Манго");
$fruits[] = "Киви"; // Альтернативный способ

// Удаление последнего элемента
$last = array_pop($fruits);

// Удаление первого элемента
$first = array_shift($fruits);

// Добавление в начало
array_unshift($fruits, "Ананас");

print_r($fruits);
?>
