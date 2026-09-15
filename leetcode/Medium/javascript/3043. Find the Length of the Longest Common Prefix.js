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
 * Находит длину самого длинного общего префикса среди всех пар (x, y),
 * где x из arr1, y из arr2.
 * 
 * Префикс числа — это число, образованное одной или несколькими его
 * начальными цифрами (например, 123 — префикс 12345).
 * 
 * Алгоритм:
 * 1. Собрать все возможные префиксы чисел из arr1 в Set.
 * 2. Для каждого числа из arr2 проверять его префиксы (от самого
 *    длинного к короткому) на наличие в Set.
 *    При первом совпадении обновить максимальную длину и перейти
 *    к следующему числу (т.к. более короткие префиксы не дадут
 *    большей длины).
 * 
 * Сложность: O((N+M)*L) по времени, O(N*L) по памяти.
 * 
 * @param {number[]} arr1 - Первый массив положительных целых чисел
 * @param {number[]} arr2 - Второй массив положительных целых чисел
 * @return {number} Максимальная длина общего префикса среди всех пар
 */
var longestCommonPrefix = function(arr1, arr2) {
    // Шаг 1: собираем все префиксы чисел из arr1
    const prefixes = new Set();
    for (let x of arr1) {
        while (x > 0) {
            prefixes.add(x);
            x = Math.floor(x / 10);
        }
    }

    let maxLen = 0;

    // Шаг 2: проверяем префиксы чисел из arr2
    for (let y of arr2) {
        while (y > 0) {
            if (prefixes.has(y)) {
                // Нашли совпадение — обновляем максимум и переходим дальше
                maxLen = Math.max(maxLen, String(y).length);
                break;
            }
            y = Math.floor(y / 10);
        }
    }

    return maxLen;
};