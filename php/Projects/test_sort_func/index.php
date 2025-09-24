<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Практика: Функции для работы с массивами</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        h1, h2 {
            color: #2c3e50;
        }
        .container {
            background-color: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .example {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        pre {
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .practice {
            margin-top: 30px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #2980b9;
        }
        .result {
            background-color: #e8f4fc;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            border-left: 4px solid #3498db;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Встроенные функции для работы с массивами в PHP</h1>
        
        <div class="example">
            <h2>Практика: Сортировка массива</h2>
            <p>Введите числа через запятую и выберите тип сортировки:</p>
            
            <form method="POST" action="">
                <div class="form-group">
                    <label for="numbers">Числа:</label>
                    <input type="text" id="numbers" name="numbers" placeholder="Например: 5, 2, 8, 10, 3" required>
                </div>
                
                <div class="form-group">
                    <label>Тип сортировки:</label><br>
                    <input type="radio" id="sort" name="sort_type" value="sort" checked>
                    <label for="sort">По возрастанию (sort)</label><br>
                    
                    <input type="radio" id="rsort" name="sort_type" value="rsort">
                    <label for="rsort">По убыванию (rsort)</label><br>
                    
                    <input type="radio" id="asort" name="sort_type" value="asort">
                    <label for="asort">По значению (asort)</label><br>
                    
                    <input type="radio" id="ksort" name="sort_type" value="ksort">
                    <label for="ksort">По ключу (ksort)</label>
                </div>
                
                <button type="submit" name="submit_sort">Отсортировать</button>
            </form>
            
            <?php
            if (isset($_POST['submit_sort'])) {
                $input = $_POST['numbers'];
                $sort_type = $_POST['sort_type'];
                
                // Преобразуем введенные данные в массив чисел
                $numbersArray = array_map('intval', explode(',', $input));
                
                echo '<div class="result">';
                echo '<h3>Результат:</h3>';
                echo '<p><strong>Исходный массив:</strong> ' . implode(', ', $numbersArray) . '</p>';
                
                // Выполняем выбранную сортировку
                switch ($sort_type) {
                    case 'sort':
                        sort($numbersArray);
                        echo '<p><strong>Отсортированный массив (по возрастанию):</strong> ' . implode(', ', $numbersArray) . '</p>';
                        break;
                    case 'rsort':
                        rsort($numbersArray);
                        echo '<p><strong>Отсортированный массив (по убыванию):</strong> ' . implode(', ', $numbersArray) . '</p>';
                        break;
                    case 'asort':
                        // Создаем ассоциативный массив для демонстрации asort
                        $assocArray = [];
                        foreach ($numbersArray as $index => $value) {
                            $assocArray["Элемент $index"] = $value;
                        }
                        asort($assocArray);
                        echo '<p><strong>Отсортированный ассоциативный массив (по значению):</strong><br>';
                        foreach ($assocArray as $key => $value) {
                            echo "$key: $value<br>";
                        }
                        echo '</p>';
                        break;
                    case 'ksort':
                        // Создаем ассоциативный массив для демонстрации ksort
                        $assocArray = [];
                        foreach ($numbersArray as $index => $value) {
                            $assocArray["Ключ $index"] = $value;
                        }
                        ksort($assocArray);
                        echo '<p><strong>Отсортированный ассоциативный массив (по ключу):</strong><br>';
                        foreach ($assocArray as $key => $value) {
                            echo "$key: $value<br>";
                        }
                        echo '</p>';
                        break;
                }
                
                echo '</div>';
            }
            ?>
        </div>
        
        <div class="example">
            <h2>Практика: Поиск в массиве</h2>
            <p>Введите элементы массива через запятую и значение для поиска:</p>
            
            <form method="POST" action="">
                <div class="form-group">
                    <label for="search_array">Элементы массива:</label>
                    <input type="text" id="search_array" name="search_array" placeholder="Например: яблоко, апельсин, банан" required>
                </div>
                
                <div class="form-group">
                    <label for="search_value">Значение для поиска:</label>
                    <input type="text" id="search_value" name="search_value" required>
                </div>
                
                <button type="submit" name="submit_search">Найти</button>
            </form>
            
            <?php
            if (isset($_POST['submit_search'])) {
                $arrayInput = $_POST['search_array'];
                $searchValue = $_POST['search_value'];
                
                // Преобразуем введенные данные в массив
                $searchArray = array_map('trim', explode(',', $arrayInput));
                
                echo '<div class="result">';
                echo '<h3>Результат:</h3>';
                echo '<p><strong>Массив:</strong> ' . implode(', ', $searchArray) . '</p>';
                echo '<p><strong>Значение для поиска:</strong> ' . $searchValue . '</p>';
                
                // Выполняем поиск
                if (in_array($searchValue, $searchArray)) {
                    $key = array_search($searchValue, $searchArray);
                    echo '<p><strong>Результат:</strong> Значение найдено! Ключ: ' . $key . '</p>';
                } else {
                    echo '<p><strong>Результат:</strong> Значение не найдено в массиве.</p>';
                }
                
                echo '</div>';
            }
            ?>
        </div>
    </div>
</body>
</html>