/**
 * Решение задачи "Count Square Sum Triples" (LeetCode 1925)
 * 
 * @fileoverview Алгоритм подсчёта упорядоченных пифагоровых троек
 * @description Подсчёт троек (a, b, c) таких, что a² + b² = c², 1 ≤ a,b,c ≤ n
 * 
 * @author Дулей Максим Игоревич
 * @see {@link https://orcid.org/0009-0007-7605-539X|ORCID}
 * @see {@link https://github.com/QuadDarv1ne/|GitHub}
 * 
 * @complexity
 * - Время: O(n²)
 * - Память: O(1) для базового решения, O(n) для оптимизированного
 */

/**
 * Подсчитывает количество упорядоченных пифагоровых троек
 * 
 * @param {number} n - Верхняя граница диапазона (1 ≤ n ≤ 250)
 * @returns {number} Количество троек, удовлетворяющих a² + b² = c²
 * 
 * @example
 * // Возвращает 2
 * countTriples(5);
 * 
 * @example
 * // Возвращает 4
 * countTriples(10);
 * 
 * @algorithm
 * 1. Для каждой пары (a, b) вычисляем сумму квадратов
 * 2. Находим целую часть квадратного корня
 * 3. Проверяем, что квадрат этой части равен сумме и c ≤ n
 * 4. Учитываем упорядоченность троек
 */
function countTriples(n) {
    let count = 0;
    
    for (let a = 1; a <= n; a++) {
        for (let b = 1; b <= n; b++) {
            const c_sq = a * a + b * b;
            const c = Math.floor(Math.sqrt(c_sq));
            
            if (c <= n && c * c === c_sq) {
                count++;
            }
        }
    }
    
    return count;
}

/**
 * Оптимизированная версия с использованием Set
 * 
 * @param {number} n - Верхняя граница диапазона
 * @returns {number} Количество троек
 */
function countTriplesOptimized(n) {
    const squares = new Set();
    
    // Предварительно вычисляем все квадраты
    for (let i = 1; i <= n; i++) {
        squares.add(i * i);
    }
    
    let count = 0;
    const maxSquare = n * n;
    const squaresArray = Array.from(squares);
    
    // Перебираем все пары квадратов
    for (const a_sq of squaresArray) {
        for (const b_sq of squaresArray) {
            const sum = a_sq + b_sq;
            if (sum <= maxSquare && squares.has(sum)) {
                count++;
            }
        }
    }
    
    return count;
}

/**
 * Версия с массивом для быстрой проверки
 * 
 * @param {number} n - Верхняя граница диапазона
 * @returns {number} Количество троек
 */
function countTriplesArray(n) {
    const maxSquare = n * n;
    const isPerfectSquare = new Array(maxSquare + 1).fill(false);
    
    // Отмечаем совершенные квадраты
    for (let i = 1; i <= n; i++) {
        isPerfectSquare[i * i] = true;
    }
    
    let count = 0;
    
    // Перебираем все пары (a, b)
    for (let a = 1; a <= n; a++) {
        const a_sq = a * a;
        for (let b = 1; b <= n; b++) {
            const sum = a_sq + b * b;
            if (sum <= maxSquare && isPerfectSquare[sum]) {
                count++;
            }
        }
    }
    
    return count;
}

/**
 * Расширенная версия с возвратом информации о тройках
 * 
 * @param {number} n - Верхняя граница диапазона
 * @returns {Object} Объект с количеством и списком троек
 */
function countTriplesWithDetails(n) {
    const triples = [];
    let count = 0;
    
    for (let a = 1; a <= n; a++) {
        for (let b = 1; b <= n; b++) {
            const c_sq = a * a + b * b;
            const c = Math.floor(Math.sqrt(c_sq));
            
            if (c <= n && c * c === c_sq) {
                count++;
                triples.push([a, b, c]);
            }
        }
    }
    
    return {
        count: count,
        triples: triples,
        formula: 'a² + b² = c²',
        range: `1 ≤ a,b,c ≤ ${n}`
    };
}

// Тестирование
function testCountTriples() {
    console.log("Тестирование Count Square Sum Triples:");
    console.log("======================================");
    
    const testCases = [
        { n: 5, expected: 2 },
        { n: 10, expected: 4 },
        { n: 1, expected: 0 },
        { n: 2, expected: 0 },
        { n: 13, expected: 6 },
        { n: 250, expected: 650 }
    ];
    
    let allPassed = true;
    
    for (const test of testCases) {
        const result = countTriples(test.n);
        const passed = result === test.expected;
        allPassed = allPassed && passed;
        
        console.log(`${passed ? '✓' : '✗'} n=${test.n}: ${result} (ожидалось ${test.expected})`);
    }
    
    console.log("======================================");
    console.log(allPassed ? "Все тесты пройдены!" : "Некоторые тесты не прошли.");
    
    // Демонстрация работы с деталями
    console.log("\nДетальная информация для n=10:");
    const details = countTriplesWithDetails(10);
    console.log(`Количество: ${details.count}`);
    console.log(`Диапазон: ${details.range}`);
    console.log("Тройки:");
    for (const triple of details.triples) {
        console.log(`  (${triple[0]}, ${triple[1]}, ${triple[2]})`);
    }
}

// Запуск тестов
if (typeof window === 'undefined') {
    // Node.js окружение
    testCountTriples();
} else {
    // Браузерное окружение
    console.log("Функции countTriples доступны для использования");
    console.log("Используйте testCountTriples() для запуска тестов");
}