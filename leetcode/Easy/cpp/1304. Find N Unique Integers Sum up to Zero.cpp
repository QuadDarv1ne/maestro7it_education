/**
 * https://leetcode.com/problems/find-n-unique-integers-sum-up-to-zero/description/?envType=daily-question&envId=2025-09-07
 */

#include <vector>
using namespace std;

/**
 * Возвращает вектор из n уникальных целых чис, сумма которых равна нулю.
 * Идея: заполняем последовательность вида [-(n-1), …, (n-1)] с шагом 2.
 * Это гарантирует n элементов и сумму 0.
 */
class Solution {
public:
    vector<int> sumZero(int n) {
        vector<int> ans(n);
        for (int i = 0; i < n; ++i) {
            ans[i] = i * 2 - n + 1;
        }
        return ans;
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