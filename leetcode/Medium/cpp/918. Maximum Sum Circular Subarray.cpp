/**
 * https://leetcode.com/problems/maximum-sum-circular-subarray/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <vector>
#include <numeric>
#include <algorithm>

using namespace std;

class Solution {
public:
    /**
     * Метод возвращает максимальную сумму подмассива в кольцевом массиве.
     * Кольцевой массив — это массив, где конец соединён с началом,
     * поэтому подмассив может «перекрываться» через границу массива.
     *
     * @param nums Вектор целых чисел — входной массив.
     * @return Максимальная сумма подмассива с учётом кольцевой структуры.
     */
    int maxSubarraySumCircular(vector<int>& nums) {
        int total_sum = accumulate(nums.begin(), nums.end(), 0);
        int max_sum = kadane(nums, false);
        int min_sum = kadane(nums, true);
        if (total_sum == min_sum)  // Все числа отрицательные
            return max_sum;
        return max(max_sum, total_sum - min_sum);
    }

private:
    /**
     * Вспомогательный метод алгоритма Кадане.
     * Если find_min == false — ищет максимальную сумму подмассива.
     * Если find_min == true — ищет минимальную сумму подмассива.
     *
     * @param nums Входной вектор целых чисел.
     * @param find_min Флаг поиска минимальной суммы.
     * @return Максимальная или минимальная сумма подмассива.
     */
    int kadane(const vector<int>& nums, bool find_min) {
        int curr_sum = nums[0];
        int result = nums[0];
        for (int i = 1; i < (int)nums.size(); ++i) {
            if (find_min) {
                curr_sum = min(nums[i], curr_sum + nums[i]);
                result = min(result, curr_sum);
            } else {
                curr_sum = max(nums[i], curr_sum + nums[i]);
                result = max(result, curr_sum);
            }
        }
        return result;
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/