/**
 * https://leetcode.com/problems/count-elements-with-maximum-frequency/description/?envType=daily-question&envId=2025-09-22
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Подсчёт элементов с максимальной частотой встречаемости.
    /// 
    /// Алгоритм:
    /// 1. Подсчитать частоты всех элементов массива.
    /// 2. Найти максимальное значение частоты.
    /// 3. Вернуть количество различных элементов, имеющих эту частоту.
    /// </summary>
    /// <param name="nums">Входной массив целых чисел</param>
    /// <returns>Количество элементов с максимальной частотой</returns>
    public int MaxFrequencyElements(int[] nums) {
        var freq = new Dictionary<int,int>();
        foreach(int x in nums) {
            if(freq.ContainsKey(x)) freq[x]++; else freq[x] = 1;
        }
        int maxFreq = 0;
        foreach(var kv in freq) if(kv.Value > maxFreq) maxFreq = kv.Value;
        int result = 0;
        foreach(var kv in freq) if(kv.Value == maxFreq) result += kv.Value;
        return result;
    }
}


/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/