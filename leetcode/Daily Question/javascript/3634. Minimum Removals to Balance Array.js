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

// JavaScript
var minRemoval = function(nums, k) {
    /*
     * Находит минимальное количество элементов для удаления, чтобы сделать массив сбалансированным.
     * Массив считается сбалансированным, если max <= min * k.
     * 
     * Подход: Сортируем массив, затем используем скользящее окно для поиска
     * самого длинного подмассива, удовлетворяющего условию.
     * 
     * Сложность по времени: O(n log n)
     * Сложность по памяти: O(1)
     */
    nums.sort((a, b) => a - b);
    const n = nums.length;
    let maxValidLength = 0;
    let right = 0;
    
    for (let left = 0; left < n; left++) {
        while (right < n && nums[right] <= nums[left] * k) {
            right++;
        }
        
        maxValidLength = Math.max(maxValidLength, right - left);
    }
    
    return n - maxValidLength;
};