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
    /// Находит размеры коробок для обмена, чтобы у Алисы и Боба стало поровну конфет.
    /// 
    /// Алгоритм:
    /// - Вычисляем общую сумму конфет у Алисы и Боба.
    /// - Находим разницу diff = (sumA - sumB) / 2.
    /// - Для каждой коробки Алисы a вычисляем необходимую коробку Боба b = a - diff.
    /// - Если b есть у Боба (хранится в хеш-множестве), возвращаем [a, b].
    /// </summary>
    /// <param name="aliceSizes">массив коробок Алисы</param>
    /// <param name="bobSizes">массив коробок Боба</param>
    /// <returns>массив из двух чисел [коробка_Алисы, коробка_Боба]</returns>
    public int[] FairCandySwap(int[] aliceSizes, int[] bobSizes) {
        int sumA = aliceSizes.Sum();
        int sumB = bobSizes.Sum();
        int diff = (sumA - sumB) / 2;
        HashSet<int> setB = new HashSet<int>(bobSizes);
        foreach (int a in aliceSizes) {
            int need = a - diff;
            if (setB.Contains(need))
                return new int[] { a, need };
        }
        return new int[] { 0, 0 };
    }
}