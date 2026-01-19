/*
LeetCode 137: Single Number II

Задача: Дан массив целых чисел nums, где каждый элемент встречается три раза,
кроме одного, который встречается ровно один раз. Найти этот единственный элемент.

Ограничения:
- Линейная временная сложность O(n)
- Константная дополнительная память O(1)

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1: @quadd4rv1n7
3. Telegram №2: @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
*/

/**
 * Подход 1: Побитовая манипуляция - Подсчет битов (Самый интуитивный)
 * Время: O(32n) = O(n), Память: O(1)
 * 
 * Для каждой битовой позиции подсчитываем, сколько чисел имеют 1 в этой позиции.
 * Если count % 3 != 0, то единственное число имеет 1 в этой позиции.
 * 
 * @param {number[]} nums
 * @return {number}
 */
var singleNumberBitCount = function(nums) {
    let result = 0;
    
    for (let i = 0; i < 32; i++) {
        let count = 0;
        for (let num of nums) {
            // Подсчитываем, сколько чисел имеют установленный бит i
            count += (num >> i) & 1;
        }
        
        // Если count не делится на 3, единственное число имеет этот бит
        if (count % 3) {
            if (i === 31) {  // Обработка отрицательных чисел (знаковый бит)
                result -= (1 << i);
            } else {
                result |= (1 << i);
            }
        }
    }
    
    return result;
};

/**
 * Подход 2: Цифровая логика - Конечный автомат (Наиболее оптимальный)
 * Время: O(n), Память: O(1)
 * 
 * Используем две переменные (ones, twos) для отслеживания битов, 
 * которые появились 1 или 2 раза.
 * Когда бит появляется 3 раза, сбрасываем обе переменные для этого бита.
 * 
 * Переходы состояний:
 * - Видим число первый раз -> идет в 'ones'
 * - Видим число второй раз -> переходит из 'ones' в 'twos'
 * - Видим число третий раз -> удаляется из обоих 'ones' и 'twos'
 * 
 * @param {number[]} nums
 * @return {number}
 */
var singleNumber = function(nums) {
    let ones = 0;  // Биты, которые появились один раз
    let twos = 0;  // Биты, которые появились два раза
    
    for (let num of nums) {
        // Добавляем в twos, если уже было в ones
        twos |= ones & num;
        
        // XOR с ones (переключаем бит)
        ones ^= num;
        
        // Если бит присутствует и в ones, и в twos, он появился 3 раза
        // Удаляем его из обеих переменных
        let common = ones & twos;
        ones &= ~common;
        twos &= ~common;
    }
    
    return ones;
};

/**
 * Подход 3: Хеш-таблица (Не удовлетворяет требованию по памяти, но легко понять)
 * Время: O(n), Память: O(n)
 * 
 * Подсчитываем вхождения с помощью объекта/Map.
 * Возвращаем число с count == 1.
 * 
 * @param {number[]} nums
 * @return {number}
 */
var singleNumberHashMap = function(nums) {
    const count = new Map();
    
    for (let num of nums) {
        count.set(num, (count.get(num) || 0) + 1);
    }
    
    for (let [num, cnt] of count.entries()) {
        if (cnt === 1) {
            return num;
        }
    }
    
    return -1;
};