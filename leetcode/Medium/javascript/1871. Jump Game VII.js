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
 * @param {string} s - Бинарная строка.
 * @param {number} minJump - Минимальная длина прыжка.
 * @param {number} maxJump - Максимальная длина прыжка.
 * @return {boolean} - Возможно ли достичь последнего индекса.
 * 
 * @description
 * Решение задачи Jump Game VII.
 * 
 * Задача состоит в том, чтобы добраться от индекса 0 до последнего индекса строки.
 * Прыжок можно совершить с индекса i на j, если i < j <= i + maxJump,
 * j >= i + minJump и s[j] == '0'.
 * 
 * Используется подход скользящего окна (Sliding Window):
 * - dp[i] показывает, достижим ли индекс i.
 * - count хранит количество достижимых индексов в диапазоне
 *   [i - maxJump, i - minJump], которые могут привести к i.
 */
var canReach = function(s, minJump, maxJump) {
    const n = s.length;
    const dp = new Array(n).fill(false);
    dp[0] = true;
    let count = 0;

    for (let i = 1; i < n; i++) {
        // Добавляем элемент, входящий в окно справа (источник для прыжка)
        if (i >= minJump && dp[i - minJump]) {
            count++;
        }
        // Убираем элемент, выходящий из окна слева
        if (i > maxJump && dp[i - maxJump - 1]) {
            count--;
        }

        // Обновляем достижимость текущей позиции
        if (s[i] === '0' && count > 0) {
            dp[i] = true;
        }
    }

    return dp[n - 1];
};