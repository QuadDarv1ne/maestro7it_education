/**
 * https://leetcode.com/problems/find-triangular-sum-of-an-array/description/?envType=daily-question&envId=2025-09-30
 */

class Solution {
    public int triangularSum(int[] nums) {
        /*
        Симулируем процесс построения треугольной суммы:
        на каждом шаге заменяем nums на новый массив, длиной -1,
        где newNums[i] = (nums[i] + nums[i+1]) % 10.
        В конце возвращаем единственный элемент.
        */
        int n = nums.length;
        for (int length = n; length > 1; length--) {
            for (int i = 0; i < length - 1; i++) {
                nums[i] = (nums[i] + nums[i + 1]) % 10;
            }
        }
        return nums[0];
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