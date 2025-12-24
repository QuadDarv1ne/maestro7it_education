/**
 * Задача: Минимальное количество коробок для перераспределения яблок (LeetCode #3074)
 * 
 * Описание:
 * Даны два массива:
 * 1. apple - где apple[i] представляет количество яблок в i-й корзине
 * 2. capacity - где capacity[j] представляет вместимость j-й коробки
 * 
 * Необходимо найти минимальное количество коробок, достаточное для упаковки всех яблок.
 * 
 * Автор: Дуплей Максим Игоревич
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
 * 
 * Сложность:
 * - Время: O(n log n) из-за сортировки
 * - Память: O(1) (не считая входных данных)
 */

using System;
using System.Linq;

public class Solution {
    public int MinimumBoxes(int[] apple, int[] capacity) {
        // Считаем общее количество яблок
        int totalApples = apple.Sum();
        
        // Сортируем коробки по убыванию вместимости
        Array.Sort(capacity);
        Array.Reverse(capacity);
        
        // Жадный алгоритм: берем самые вместительные коробки
        int currentCapacity = 0;
        int boxesUsed = 0;
        
        foreach (int boxCapacity in capacity) {
            boxesUsed++;
            currentCapacity += boxCapacity;
            
            // Если набрали достаточную вместимость
            if (currentCapacity >= totalApples) {
                return boxesUsed;
            }
        }
        
        return boxesUsed; // Теоретически недостижимо
    }
}