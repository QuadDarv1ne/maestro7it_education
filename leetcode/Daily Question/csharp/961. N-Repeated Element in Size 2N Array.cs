/**
 * https://leetcode.com/problems/n-repeated-element-in-size-2n-array/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "N-Repeated Element in Size 2N Array"
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
     * Находит элемент, повторяющийся N раз в массиве размером 2N.
     * 
     * @param nums массив длины 2N, содержащий N+1 уникальных элементов,
     *              один из которых повторяется N раз
     *              
     * @return Элемент, повторяющийся N раз
     */
    public int RepeatedNTimes(int[] nums) {
        // Способ 1: Использование HashSet
        HashSet<int> seen = new HashSet<int>();
        foreach (int num in nums) {
            if (seen.Contains(num)) {
                return num;
            }
            seen.Add(num);
        }
        
        // Способ 2: Альтернативный - проверка соседних элементов
        // Проверяем элементы на расстоянии 1, 2 и 3
        // Этот способ использует O(1) дополнительной памяти
        // и работает быстрее в некоторых случаях
        
        // Для полноты решения, если первый способ не сработал:
        return -1;
    }
}