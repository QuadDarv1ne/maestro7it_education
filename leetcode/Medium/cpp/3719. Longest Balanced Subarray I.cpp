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
    /**
     * Находит длину самого длинного сбалансированного подмассива.
     * 
     * Подмассив считается сбалансированным, если количество уникальных
     * четных чисел равно количеству уникальных нечетных чисел.
     * 
     * @param nums Входной вектор целых чисел
     * @return Длина самого длинного сбалансированного подмассива
     * 
     * Примеры:
     *   longestBalanced([2,5,4,3]) → 4
     *   longestBalanced([3,2,2,5,4]) → 5
     *   longestBalanced([1,2,3,2]) → 3
     */
    int longestBalanced(vector<int>& nums) {
        int n = nums.size();
        int max_len = 0;
        
        for (int i = 0; i < n; i++) {
            unordered_set<int> even_set;
            unordered_set<int> odd_set;
            
            for (int j = i; j < n; j++) {
                if (nums[j] % 2 == 0) {
                    even_set.insert(nums[j]);
                } else {
                    odd_set.insert(nums[j]);
                }
                
                if (even_set.size() == odd_set.size()) {
                    max_len = max(max_len, j - i + 1);
                }
            }
        }
        
        return max_len;
    }
};