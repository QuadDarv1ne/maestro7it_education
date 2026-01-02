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

import java.util.HashSet;
import java.util.Set;

class Solution {
    /**
     * Находит элемент, повторяющийся N раз в массиве размером 2N.
     * 
     * @param nums массив длины 2N, содержащий N+1 уникальных элементов,
     *              один из которых повторяется N раз
     *              
     * @return Элемент, повторяющийся N раз
     */
    public int repeatedNTimes(int[] nums) {
        // Способ 1: Использование HashSet
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (seen.contains(num)) {
                return num;
            }
            seen.add(num);
        }
        
        // Способ 2: Альтернативный - проверка соседних элементов
        // Проверяем элементы на расстоянии 1, 2 и 3
        // Это работает, потому что в массиве длиной 2N
        // повторяющийся элемент не может быть разделен
        // более чем 3 уникальными элементами
        
        // Для полноты решения, если первый способ не сработал:
        return -1;
    }
}