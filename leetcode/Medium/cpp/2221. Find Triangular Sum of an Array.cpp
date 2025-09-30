/**
 * https://leetcode.com/problems/find-triangular-sum-of-an-array/description/?envType=daily-question&envId=2025-09-30
 */

#include <vector>
using namespace std;

class Solution {
public:
    int triangularSum(vector<int>& nums) {
        /*
        Находит треугольную сумму массива nums:
        Повторно заменяем nums на массив меньшей длины,
        где nums[i] = (prev[i] + prev[i+1]) % 10.
        Возвращаем единственный оставшийся элемент.
        */
        int n = nums.size();
        for (int length = n; length > 1; --length) {
            for (int i = 0; i + 1 < length; ++i) {
                nums[i] = (nums[i] + nums[i + 1]) % 10;
            }
        }
        return nums[0];
    }
};

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