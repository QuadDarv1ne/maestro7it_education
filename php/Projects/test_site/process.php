<?php
// Функции для работы с массивами
function calculateSum($array) {
    return array_sum($array);
}

function calculateAverage($array) {
    return count($array) > 0 ? array_sum($array) / count($array) : 0;
}

function findMax($array) {
    return count($array) > 0 ? max($array) : 'Массив пуст';
}

function findMin($array) {
    return count($array) > 0 ? min($array) : 'Массив пуст';
}

function sortArray($array) {
    sort($array);
    return $array;
}

// Обработка данных формы
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $inputData = $_POST['numbers'] ?? '';
    $operation = $_POST['operation'] ?? 'sum';
    
    // Параметры для редиректа
    $redirectParams = [
        'numbers' => urlencode($inputData),
        'operation' => urlencode($operation)
    ];
    
    if (empty($inputData)) {
        $redirectParams['error'] = urlencode('Пожалуйста, введите числа для обработки.');
        header('Location: index.php?' . http_build_query($redirectParams));
        exit;
    }
    
    // Преобразуем введенные данные в массив чисел
    $inputArray = explode(',', $inputData);
    $numbersArray = [];
    $hasErrors = false;
    
    foreach ($inputArray as $value) {
        $trimmedValue = trim($value);
        if (is_numeric($trimmedValue)) {
            $numbersArray[] = (float)$trimmedValue;
        } else if (!empty($trimmedValue)) {
            $hasErrors = true;
        }
    }
    
    if ($hasErrors) {
        $redirectParams['error'] = urlencode('Некоторые введенные значения не являются числами и были проигнорированы.');
    }
    
    if (empty($numbersArray)) {
        $redirectParams['error'] = urlencode('Не было введено ни одного допустимого числа.');
        header('Location: index.php?' . http_build_query($redirectParams));
        exit;
    }
    
    // Выполняем выбранную операцию
    switch ($operation) {
        case 'sum':
            $result = calculateSum($numbersArray);
            break;
        case 'average':
            $result = calculateAverage($numbersArray);
            break;
        case 'max':
            $result = findMax($numbersArray);
            break;
        case 'min':
            $result = findMin($numbersArray);
            break;
        case 'sort':
            $result = implode(', ', sortArray($numbersArray));
            break;
        default:
            $result = 'Неизвестная операция';
    }
    
    $redirectParams['result'] = urlencode($result);
    
    // Редирект с результатом
    header('Location: index.php?' . http_build_query($redirectParams));
    exit;
} else {
    // Если запрос не POST, перенаправляем на главную
    header('Location: index.php');
    exit;
}
?>