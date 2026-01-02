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

#include <vector>
#include <unordered_set>
using namespace std;

class Solution {
public:
    int repeatedNTimes(vector<int>& nums) {
        /**
         * Находит элемент, повторяющийся N раз в массиве размером 2N.
         * 
         * @param nums вектор длины 2N, содержащий N+1 уникальных элементов,
         *              один из которых повторяется N раз
         *              
         * @return Элемент, повторяющийся N раз
         */
        
        // Способ 1: Использование unordered_set (хеш-таблицы)
        unordered_set<int> seen;
        for (int num : nums) {
            if (seen.find(num) != seen.end()) {
                return num;
            }
            seen.insert(num);
        }
        
        // Способ 2: Альтернативный - проверка соседних элементов
        // Поскольку массив имеет длину 2N, а один элемент повторяется N раз,
        // то между одинаковыми элементами максимальное расстояние может быть 3.
        // Это можно использовать для оптимизации памяти до O(1).
        
        // Для полноты решения, если первый способ не сработал:
        return -1;
    }
};