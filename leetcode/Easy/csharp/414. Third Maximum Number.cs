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
    /// Возвращает третий уникальный максимум или максимум, если уникальных меньше трёх.
    /// </summary>
    /// <param name="nums">Массив целых чисел.</param>
    /// <returns>Третий уникальный максимум или максимальное число.</returns>
    public int ThirdMax(int[] nums) {
        // Используем long? (nullable) для обозначения отсутствия значения
        long? first = null, second = null, third = null;

        foreach (int num in nums) {
            if (num == first || num == second || num == third) continue;

            if (first == null || num > first) {
                third = second;
                second = first;
                first = num;
            } else if (second == null || num > second) {
                third = second;
                second = num;
            } else if (third == null || num > third) {
                third = num;
            }
        }

        return third.HasValue ? (int)third : (int)first;
    }
}