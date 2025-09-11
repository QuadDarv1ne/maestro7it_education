/**
 * https://leetcode.com/problems/sort-vowels-in-a-string/description/?envType=daily-question&envId=2025-09-11
 */

/**
 * Функция sortVowels принимает строку и сортирует все гласные буквы
 * в порядке возрастания (по Unicode), оставляя остальные символы на местах.
 *
 * Алгоритм:
 * 1. Извлечь все гласные в массив.
 * 2. Отсортировать их.
 * 3. Подставить обратно на позиции гласных.
 *
 * Временная сложность: O(n log n).
 *
 * @param {string} s - исходная строка
 * @return {string} - новая строка с отсортированными гласными
 */
var sortVowels = function(s) {
    const isVowel = c => "aeiouAEIOU".includes(c);
    let vowels = [];
    for (let c of s) {
        if (isVowel(c)) vowels.push(c);
    }
    vowels.sort((a, b) => a.localeCompare(b));
    let vi = 0;
    let result = [...s];
    for (let i = 0; i < result.length; i++) {
        if (isVowel(result[i])) {
            result[i] = vowels[vi++];
        }
    }
    return result.join('');
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/