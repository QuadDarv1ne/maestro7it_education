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

class Solution {
    /**
     * Возвращает массив количества единичных битов для чисел от 0 до n.
     * Используется подход динамического программирования с битовыми операциями.
     *
     * @param n верхняя граница диапазона
     * @return массив длиной n+1, где ans[i] — число единичных битов в i
     */
    public int[] countBits(int n) {
        int[] ans = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            // ans[i >> 1] даёт результат для числа без младшего бита,
            // (i & 1) добавляет единицу, если младший бит был 1 (нечётное i)
            ans[i] = ans[i >> 1] + (i & 1);
        }
        return ans;
    }
}