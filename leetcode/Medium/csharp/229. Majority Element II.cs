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

using System;
using System.Collections.Generic;

public class Solution {
    /**
     * Находит все элементы, которые встречаются более чем ⌊ n/3 ⌋ раз.
     * 
     * Алгоритм (алгоритм Бойера-Мура для k = n/3):
     * 1. Не может быть более 2 элементов, удовлетворяющих условию.
     * 2. Используем двух кандидатов и их счетчики.
     * 3. Первый проход: находим двух кандидатов.
     * 4. Второй проход: проверяем, действительно ли кандидаты встречаются > n/3 раз.
     * 
     * Сложность:
     * Время: O(n), два прохода по массиву
     * Пространство: O(1), используем только фиксированное количество переменных
     * 
     * @param nums Входной массив целых чисел
     * @return Список элементов, встречающихся более чем ⌊ n/3 ⌋ раз
     * 
     * Примеры:
     * MajorityElement([3,2,3]) → [3]
     * MajorityElement([1]) → [1]
     * MajorityElement([1,2]) → [1,2]
     * MajorityElement([1,1,1,3,3,2,2,2]) → [1,2]
     */
    public IList<int> MajorityElement(int[] nums) {
        var result = new List<int>();
        if (nums == null || nums.Length == 0) {
            return result;
        }
        
        // Инициализация кандидатов и счетчиков
        int? candidate1 = null, candidate2 = null;
        int count1 = 0, count2 = 0;
        
        // Первый проход: поиск кандидатов
        foreach (int num in nums) {
            if (candidate1.HasValue && num == candidate1.Value) {
                count1++;
            } else if (candidate2.HasValue && num == candidate2.Value) {
                count2++;
            } else if (count1 == 0) {
                candidate1 = num;
                count1 = 1;
            } else if (count2 == 0) {
                candidate2 = num;
                count2 = 1;
            } else {
                count1--;
                count2--;
            }
        }
        
        // Второй проход: проверка кандидатов
        count1 = 0;
        count2 = 0;
        int n = nums.Length;
        
        foreach (int num in nums) {
            if (candidate1.HasValue && num == candidate1.Value) {
                count1++;
            } else if (candidate2.HasValue && num == candidate2.Value) {
                count2++;
            }
        }
        
        if (count1 > n / 3) {
            result.Add(candidate1.Value);
        }
        if (count2 > n / 3) {
            result.Add(candidate2.Value);
        }
        
        return result;
    }
    
    /**
     * Решение с использованием Dictionary (не соответствует ограничению O(1) памяти).
     * 
     * @param nums Входной массив
     * @return Список элементов, встречающихся более чем ⌊ n/3 ⌋ раз
     */
    public IList<int> MajorityElementHashMap(int[] nums) {
        var result = new List<int>();
        if (nums == null || nums.Length == 0) {
            return result;
        }
        
        var counter = new Dictionary<int, int>();
        int n = nums.Length;
        
        foreach (int num in nums) {
            if (counter.ContainsKey(num)) {
                counter[num]++;
            } else {
                counter[num] = 1;
            }
        }
        
        foreach (var kvp in counter) {
            if (kvp.Value > n / 3) {
                result.Add(kvp.Key);
            }
        }
        
        return result;
    }
}