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

public class Solution {
    /// <summary>
    /// Находит максимальное расстояние между двумя последовательными единицами
    /// в двоичном представлении числа n.
    /// </summary>
    /// <param name="n">положительное целое число (1 <= n <= 10^9)</param>
    /// <returns>максимальное расстояние, или 0, если единиц меньше двух</returns>
    public int BinaryGap(int n) {
        string binary = Convert.ToString(n, 2); // двоичное представление
        int lastIndex = -1;
        int maxDist = 0;

        for (int i = 0; i < binary.Length; i++) {
            if (binary[i] == '1') {
                if (lastIndex != -1) {
                    int dist = i - lastIndex;
                    if (dist > maxDist) maxDist = dist;
                }
                lastIndex = i;
            }
        }
        return maxDist;
    }
}