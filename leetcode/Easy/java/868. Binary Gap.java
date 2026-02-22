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
     * Находит максимальное расстояние между двумя последовательными единицами
     * в двоичном представлении числа n.
     *
     * @param n положительное целое число (1 <= n <= 10^9)
     * @return максимальное расстояние, или 0, если единиц меньше двух
     */
    public int binaryGap(int n) {
        String binary = Integer.toBinaryString(n); // двоичное представление без ведущих нулей
        int lastIndex = -1;   // позиция последней встреченной единицы
        int maxDist = 0;       // максимальное расстояние

        for (int i = 0; i < binary.length(); i++) {
            if (binary.charAt(i) == '1') {
                if (lastIndex != -1) {
                    int dist = i - lastIndex;
                    if (dist > maxDist) {
                        maxDist = dist;
                    }
                }
                lastIndex = i;
            }
        }
        return maxDist;
    }
}