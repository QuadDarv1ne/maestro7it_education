/**
 * @file Решение задачи LeetCode 1984. Minimum Difference Between Highest and Lowest of K Scores
 * @see {@link https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/}
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

#include <vector>
#include <algorithm>
#include <climits>

class Solution {
public:
    int minimumDifference(vector<int>& nums, int k) {
        /**
         * Алгоритм находит минимальную возможную разницу между наибольшим и 
         * наименьшим значением в любой группе из k элементов массива.
         * 
         * @param nums Вектор целых чисел (оценки учащихся)
         * @param k Количество элементов для выбора в группе
         * @return Минимальная возможная разница между максимальным и 
         *         минимальным значением в группе из k элементов
         * 
         * Алгоритм:
         *   1. Сортировка массива по возрастанию
         *   2. Использование скользящего окна размера k для нахождения 
         *      минимальной разницы между первым и последним элементом
         *   3. Возврат минимальной найденной разницы
         * 
         * Сложность:
         *   Время: O(n log n) - доминирует операция сортировки
         *   Память: O(1) - сортировка на месте
         * 
         * Примеры:
         *   vector<int> nums1 = {9, 4, 1, 7};
         *   minimumDifference(nums1, 2); // Возвращает 2
         *   
         *   vector<int> nums2 = {90};
         *   minimumDifference(nums2, 1); // Возвращает 0
         *   
         *   vector<int> nums3 = {1, 3, 5, 7, 9, 11};
         *   minimumDifference(nums3, 4); // Возвращает 6
         */
        
        // Обработка тривиального случая
        if (k <= 1) return 0;
        
        // Сортируем массив для применения скользящего окна
        sort(nums.begin(), nums.end());
        
        int minDiff = INT_MAX;
        int n = nums.size();
        
        // Проходим по всем возможным позициям окна длины k
        for (int i = 0; i <= n - k; i++) {
            // Разница между максимальным и минимальным в текущем окне
            int currentDiff = nums[i + k - 1] - nums[i];
            if (currentDiff < minDiff) {
                minDiff = currentDiff;
            }
        }
        
        return minDiff;
    }
};