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
 * @param {string} s
 * @return {string}
 */
var reverseVowels = function(s) {
    // Множество гласных для быстрой проверки
    const vowels = new Set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']);
    // Преобразуем строку в массив (строки в JS неизменяемы)
    const arr = s.split('');
    let left = 0;
    let right = arr.length - 1;
    
    while (left < right) {
        // Ищем гласную слева
        while (left < right && !vowels.has(arr[left])) {
            left++;
        }
        // Ищем гласную справа
        while (left < right && !vowels.has(arr[right])) {
            right--;
        }
        // Меняем местами
        if (left < right) {
            [arr[left], arr[right]] = [arr[right], arr[left]];
            left++;
            right--;
        }
    }
    
    return arr.join('');
};