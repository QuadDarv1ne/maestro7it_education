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

public class NumArray {
    /// <summary>
    /// Массив префиксных сумм.
    /// </summary>
    private int[] prefix;

    /// <summary>
    /// Конструктор. Принимает исходный массив и вычисляет префиксные суммы.
    /// </summary>
    /// <param name="nums">Исходный массив целых чисел.</param>
    public NumArray(int[] nums) {
        prefix = new int[nums.Length + 1];
        for (int i = 0; i < nums.Length; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }
    
    /// <summary>
    /// Возвращает сумму элементов с индекса left по right включительно.
    /// </summary>
    /// <param name="left">Начальный индекс (включительно).</param>
    /// <param name="right">Конечный индекс (включительно).</param>
    /// <returns>Сумма элементов на отрезке [left, right].</returns>
    public int SumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
}