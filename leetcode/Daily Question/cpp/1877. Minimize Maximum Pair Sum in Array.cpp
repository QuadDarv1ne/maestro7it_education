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

class Solution {
public:
    int minPairSum(vector<int>& nums) {
        /**
         * Минимизирует максимальную сумму пары в массиве
         * 
         * Сортирует массив и формирует пары из первого с последним,
         * второго с предпоследним и т.д. Возвращает максимальную сумму пар.
         * 
         * Сложность: O(n log n) по времени, O(1) дополнительной памяти
         */
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int max_sum = 0;
        
        for (int i = 0; i < n / 2; i++) {
            int current_sum = nums[i] + nums[n - 1 - i];
            max_sum = max(max_sum, current_sum);
        }
        
        return max_sum;
    }
};