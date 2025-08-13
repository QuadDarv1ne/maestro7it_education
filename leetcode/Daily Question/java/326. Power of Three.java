/**
 * 326. Power of Three (Java) by Dupley Maxim Igorevich
 * https://leetcode.com/problems/power-of-three/description/?envType=daily-question&envId=2025-08-13
 */

class Solution {
    /**
     * Определяет, является ли число n степенью числа 3.
     *
     * Алгоритм:
     * - Максимальная степень числа 3, которая помещается в 32-битное целое число, равна 3^19 = 1162261467.
     * - Если n > 0 и 1162261467 делится на n без остатка, значит n является степенью числа 3.
     * - Решение работает за O(1) и не использует циклы или логарифмы.
     *
     * @param n Целое число для проверки
     * @return true если n является степенью числа 3, иначе false
     */
    public boolean isPowerOfThree(int n) {
        return n > 0 && 1162261467 % n == 0;
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/