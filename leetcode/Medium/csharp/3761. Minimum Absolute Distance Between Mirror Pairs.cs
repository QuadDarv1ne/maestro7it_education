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
    /// Находит минимальное расстояние между зеркальными парами в массиве.
    /// </summary>
    /// <param name="nums">Исходный массив целых чисел.</param>
    /// <returns>Минимальная разница индексов |i - j| или -1, если пар нет.</returns>
    public int MinMirrorPairDistance(int[] nums) {
        int minDist = int.MaxValue;
        // Ключ: число (или его перевертыш), Значение: последний индекс, где оно встретилось
        var lastSeen = new Dictionary<int, int>();
        
        for (int i = 0; i < nums.Length; i++) {
            int val = nums[i];
            
            // 1. Проверяем, является ли текущий элемент правой частью пары
            if (lastSeen.ContainsKey(val)) {
                int dist = i - lastSeen[val];
                if (dist < minDist) {
                    minDist = dist;
                }
            }
            
            // 2. Переворачиваем число и сохраняем его индекс для будущих совпадений
            char[] charArray = val.ToString().ToCharArray();
            Array.Reverse(charArray);
            int rev = int.Parse(new string(charArray));
            
            // Обновляем индекс (храним самый правый, чтобы расстояние было минимальным)
            lastSeen[rev] = i;
        }
        
        return minDist == int.MaxValue ? -1 : minDist;
    }
}