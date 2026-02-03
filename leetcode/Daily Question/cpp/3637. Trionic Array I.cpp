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
    bool isTrionic(vector<int>& nums) {
        int n = nums.size();
        if (n < 3) return false;
        
        // Вспомогательные функции как лямбды
        auto isIncreasing = [&](int start, int end) -> bool {
            for (int i = start; i < end; i++) {
                if (nums[i] >= nums[i + 1]) return false;
            }
            return true;
        };
        
        auto isDecreasing = [&](int start, int end) -> bool {
            for (int i = start; i < end; i++) {
                if (nums[i] <= nums[i + 1]) return false;
            }
            return true;
        };
        
        // Перебор всех возможных p и q
        for (int p = 1; p < n - 2; p++) {
            for (int q = p + 1; q < n - 1; q++) {
                if (isIncreasing(0, p) &&
                    isDecreasing(p, q) &&
                    isIncreasing(q, n - 1)) {
                    return true;
                }
            }
        }
        return false;
    }
};