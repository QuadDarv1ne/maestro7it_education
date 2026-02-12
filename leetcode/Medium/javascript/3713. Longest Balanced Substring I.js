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
 * @return {number}
 *
 * Возвращает длину самой длинной сбалансированной подстроки.
 * Сбалансированная подстрока — все различные символы встречаются
 * одинаковое количество раз.
 *
 * Алгоритм: полный перебор всех подстрок.
 * Для каждого левого индекса i проходим по правому j, обновляем
 * частоты символов. Если все ненулевые частоты равны — обновляем ответ.
 *
 * Сложность: O(26 * n^2) ≈ O(n^2) при n ≤ 1000, память O(1).
 */
var longestBalanced = function(s) {
    const n = s.length;
    let maxLen = 0;

    for (let i = 0; i < n; i++) {
        const freq = new Array(26).fill(0);
        for (let j = i; j < n; j++) {
            const idx = s.charCodeAt(j) - 'a'.charCodeAt(0);
            freq[idx]++;

            let minFreq = Infinity;
            let maxFreq = 0;
            for (let cnt of freq) {
                if (cnt > 0) {
                    minFreq = Math.min(minFreq, cnt);
                    maxFreq = Math.max(maxFreq, cnt);
                }
            }

            if (minFreq === maxFreq) {
                maxLen = Math.max(maxLen, j - i + 1);
            }
        }
    }
    return maxLen;
};