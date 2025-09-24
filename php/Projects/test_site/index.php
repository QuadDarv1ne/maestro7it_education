<?php
// Подключаем общие функции если они есть
if (file_exists('functions.php')) {
    include 'functions.php';
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Работа с массивами и формами в PHP</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Работа с массивами и формами в PHP</h1>
        
        <div class="form-section">
            <h2>Калькулятор массива чисел</h2>
            <form id="numbersForm" method="POST" action="process.php">
                <div class="form-group">
                    <label for="numbers">Введите числа через запятую:</label>
                    <input type="text" id="numbers" name="numbers" 
                           value="<?php echo isset($_GET['numbers']) ? htmlspecialchars($_GET['numbers']) : ''; ?>" 
                           placeholder="Например: 5, 2, 8, 10, 3" required>
                </div>
                
                <div class="form-group">
                    <label for="operation">Выберите операцию:</label>
                    <select id="operation" name="operation">
                        <option value="sum" <?php echo (isset($_GET['operation']) && $_GET['operation'] == 'sum') ? 'selected' : ''; ?>>Сумма</option>
                        <option value="average" <?php echo (isset($_GET['operation']) && $_GET['operation'] == 'average') ? 'selected' : ''; ?>>Среднее значение</option>
                        <option value="max" <?php echo (isset($_GET['operation']) && $_GET['operation'] == 'max') ? 'selected' : ''; ?>>Максимальное значение</option>
                        <option value="min" <?php echo (isset($_GET['operation']) && $_GET['operation'] == 'min') ? 'selected' : ''; ?>>Минимальное значение</option>
                        <option value="sort" <?php echo (isset($_GET['operation']) && $_GET['operation'] == 'sort') ? 'selected' : ''; ?>>Сортировка</option>
                    </select>
                </div>
                
                <button type="submit" name="submit">Выполнить</button>
            </form>
        </div>

        <?php if (isset($_GET['error'])): ?>
            <div class="result error">
                <h3>Ошибка:</h3>
                <p><?php echo htmlspecialchars($_GET['error']); ?></p>
            </div>
        <?php endif; ?>

        <?php if (isset($_GET['result'])): ?>
            <div class="result">
                <h3>Результат:</h3>
                <p><strong>Введенные числа:</strong> <?php echo isset($_GET['numbers']) ? htmlspecialchars($_GET['numbers']) : ''; ?></p>
                <p><strong>Результат операции:</strong> <?php echo htmlspecialchars($_GET['result']); ?></p>
            </div>
        <?php endif; ?>

        <div class="examples-section">
            <h2>Примеры работы с массивами и циклами</h2>
            <div class="example">
                <h3>Демонстрация работы с массивами</h3>
                <?php
                // Демонстрационный массив
                $demoArray = [10, 5, 8, 3, 12, 7];
                echo "<p><strong>Исходный массив:</strong> " . implode(", ", $demoArray) . "</p>";
                
                echo "<h4>Цикл for:</h4>";
                echo "<ul>";
                for ($i = 0; $i < count($demoArray); $i++) {
                    echo "<li>Элемент [$i] = " . $demoArray[$i] . "</li>";
                }
                echo "</ul>";
                
                echo "<h4>Цикл foreach:</h4>";
                echo "<ul>";
                foreach ($demoArray as $index => $value) {
                    echo "<li>Элемент [$index] = $value</li>";
                }
                echo "</ul>";
                
                echo "<h4>Ассоциативный массив:</h4>";
                $assocArray = [
                    "Январь" => 31,
                    "Февраль" => 28,
                    "Март" => 31,
                    "Апрель" => 30
                ];
                
                echo "<ul>";
                foreach ($assocArray as $month => $days) {
                    echo "<li>$month: $days дней</li>";
                }
                echo "</ul>";
                ?>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>