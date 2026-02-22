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
public:
    /**
     * Находит максимальное расстояние между двумя последовательными единицами
     * в двоичном представлении числа n.
     *
     * @param n положительное целое число (1 <= n <= 10^9)
     * @return максимальное расстояние, или 0, если единиц меньше двух
     */
    int binaryGap(int n) {
        int lastPos = -1;   // позиция последней единицы (считаем с 0 справа)
        int maxDist = 0;
        int pos = 0;

        while (n > 0) {
            if (n & 1) {                 // проверяем младший бит
                if (lastPos != -1) {
                    int dist = pos - lastPos;
                    if (dist > maxDist) maxDist = dist;
                }
                lastPos = pos;
            }
            n >>= 1;                     // сдвигаем вправо
            pos++;
        }
        return maxDist;
    }
};