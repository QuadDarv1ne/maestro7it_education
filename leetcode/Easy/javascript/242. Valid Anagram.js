/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * Проверяет, является ли строка t анаграммой строки s.
 * 
 * Алгоритм (подсчет символов):
 * 1. Если длины строк не равны, возвращаем false.
 * 2. Создаем массив/объект для подсчета частот символов.
 * 3. Увеличиваем счетчики для символов строки s.
 * 4. Уменьшаем счетчики для символов строки t.
 * 5. Если все счетчики равны 0, строки являются анаграммами.
 * 
 * Сложность:
 * Время: O(n)
 * Пространство: O(1) или O(k), где k - размер алфавита
 * 
 * @param {string} s - Первая строка
 * @param {string} t - Вторая строка
 * @return {boolean} true, если t является анаграммой s, иначе false
 * 
 * @example
 * isAnagram("anagram", "nagaram") // true
 * isAnagram("rat", "car") // false
 * isAnagram("", "") // true
 */
var isAnagram = function(s, t) {
    // Если длины строк разные, они не могут быть анаграммами
    if (s.length !== t.length) {
        return false;
    }
    
    // Вариант 1: Использование массива для английских букв
    const charCount = new Array(26).fill(0);
    
    for (let i = 0; i < s.length; i++) {
        charCount[s.charCodeAt(i) - 'a'.charCodeAt(0)]++;
    }
    
    for (let i = 0; i < t.length; i++) {
        const index = t.charCodeAt(i) - 'a'.charCodeAt(0);
        charCount[index]--;
        // Если счетчик стал отрицательным, значит в t больше этого символа
        if (charCount[index] < 0) {
            return false;
        }
    }
    
    // Проверяем, что все счетчики равны 0
    for (let count of charCount) {
        if (count !== 0) {
            return false;
        }
    }
    
    return true;
};

/**
 * Решение с использованием объекта (работает для любого набора символов).
 * 
 * @param {string} s - Первая строка
 * @param {string} t - Вторая строка
 * @return {boolean} true, если строки являются анаграммами
 */
var isAnagramObject = function(s, t) {
    if (s.length !== t.length) {
        return false;
    }
    
    const charCount = {};
    
    for (let char of s) {
        charCount[char] = (charCount[char] || 0) + 1;
    }
    
    for (let char of t) {
        if (!charCount[char]) {
            return false; // Символ отсутствует в s
        }
        charCount[char]--;
        if (charCount[char] < 0) {
            return false;
        }
    }
    
    // Проверяем, что все счетчики равны 0
    for (let char in charCount) {
        if (charCount[char] !== 0) {
            return false;
        }
    }
    
    return true;
};

/**
 * Решение с использованием сортировки.
 * 
 * Сложность:
 * Время: O(n log n)
 * Пространство: O(n) (или O(1) в зависимости от реализации сортировки)
 * 
 * @param {string} s - Первая строка
 * @param {string} t - Вторая строка
 * @return {boolean} true, если строки являются анаграммами
 */
var isAnagramSort = function(s, t) {
    if (s.length !== t.length) {
        return false;
    }
    
    const sSorted = s.split('').sort().join('');
    const tSorted = t.split('').sort().join('');
    
    return sSorted === tSorted;
};