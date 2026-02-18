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
     * Определяет, чередуются ли биты в двоичном представлении числа.
     *
     * @param n Положительное целое число (1 <= n <= 2^31 - 1)
     * @return true, если биты чередуются, иначе false
     *
     * Алгоритм:
     *   xorResult = n ^ (n >> 1) даёт число из всех единиц для чисел
     *   с чередующимися битами. Проверка (xorResult & (xorResult + 1)) == 0
     *   подтверждает, что xorResult состоит из всех единиц.
     *
     * Примеры:
     *   hasAlternatingBits(5)  // 101 -> true
     *   hasAlternatingBits(7)  // 111 -> false
     *   hasAlternatingBits(11) // 1011 -> false
     *
     * Сложность:
     *   Время: O(1)
     *   Память: O(1)
     */
    public boolean hasAlternatingBits(int n) {
        int xorResult = n ^ (n >> 1);
        return (xorResult & (xorResult + 1)) == 0;
    }
}