/**
 * https://leetcode.com/problems/largest-perimeter-triangle/description/?envType=daily-question&envId=2025-09-28
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int largestPerimeter(vector<int>& nums) {
        /*
        Находит максимальный периметр треугольника, который можно построить
        из трёх длин массива nums.

        Алгоритм:
        1. Сортируем массив.
        2. Идём от конца к началу: nums[i] — наибольшая сторона.
        3. Проверяем условие треугольника для троек (a, b, c).
        4. Если выполняется — возвращаем периметр.
        5. Если нет — продолжаем, иначе возвращаем 0.
        */
        sort(nums.begin(), nums.end());
        int n = nums.size();
        for (int i = n - 1; i >= 2; --i) {
            int a = nums[i - 2], b = nums[i - 1], c = nums[i];
            if (a + b > c)
                return a + b + c;
        }
        return 0;
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