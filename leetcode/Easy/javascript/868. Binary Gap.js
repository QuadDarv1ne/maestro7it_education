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
 * @param {number} n - положительное целое число (1 <= n <= 10^9)
 * @return {number} - максимальное расстояние между единицами, или 0
 */
var binaryGap = function(n) {
    const binary = n.toString(2);        // двоичная строка
    let lastIndex = -1;
    let maxDist = 0;

    for (let i = 0; i < binary.length; i++) {
        if (binary[i] === '1') {
            if (lastIndex !== -1) {
                const dist = i - lastIndex;
                if (dist > maxDist) maxDist = dist;
            }
            lastIndex = i;
        }
    }
    return maxDist;
};