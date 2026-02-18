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
    /// Определяет, чередуются ли биты в двоичном представлении числа.
    /// </summary>
    /// <param name="n">Положительное целое число (1 ≤ n ≤ 2³¹-1).</param>
    /// <returns>true, если биты чередуются, иначе false.</returns>
    /// <remarks>
    /// Алгоритм: для числа с чередующимися битами выражение n ^ (n >> 1)
    /// даёт число из всех единиц (вида 2^k - 1). Проверка (x & (x+1)) == 0
    /// подтверждает, что x состоит из всех единиц.
    /// 
    /// Примеры:
    /// HasAlternatingBits(5)  // 101 -> true
    /// HasAlternatingBits(7)  // 111 -> false
    /// HasAlternatingBits(11) // 1011 -> false
    /// 
    /// Сложность: O(1) времени и памяти.
    /// </remarks>
    public bool HasAlternatingBits(int n) {
        int xorResult = n ^ (n >> 1);
        return (xorResult & (xorResult + 1)) == 0;
    }
}