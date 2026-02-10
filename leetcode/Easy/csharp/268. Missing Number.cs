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
    /// Находит пропущенное число в диапазоне [0, n] в массиве длины n.
    /// </summary>
    /// <param name="nums">Массив длиной n, содержащий n различных чисел из [0, n]</param>
    /// <returns>Единственное пропущенное число</returns>
    /// <example>
    /// <code>
    /// MissingNumber([3,0,1]) → 2
    /// MissingNumber([0,1]) → 2
    /// MissingNumber([9,6,4,2,3,5,7,0,1]) → 8
    /// </code>
    /// </example>
    /// <remarks>
    /// Сложность:
    ///   Время: O(n)
    ///   Память: O(1)
    /// </remarks>
    public int MissingNumber(int[] nums) {
        int n = nums.Length;
        // Способ 1: Формула суммы
        int expectedSum = n * (n + 1) / 2;
        int actualSum = 0;
        foreach (int num in nums) {
            actualSum += num;
        }
        return expectedSum - actualSum;
        
        // Способ 2: XOR
        // int result = nums.Length;
        // for (int i = 0; i < nums.Length; i++) {
        //     result ^= i ^ nums[i];
        // }
        // return result;
    }
}