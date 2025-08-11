/**
 * https://leetcode.com/problems/candy/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    /**
     * Минимальное количество конфет для детей с рейтингами ratings.
     * 
     * @param ratings вектор рейтингов
     * @return минимальное число конфет
     */
    int candy(vector<int>& ratings) {
        int n = (int)ratings.size();
        vector<int> candies(n, 1);

        // Слева направо
        for (int i = 1; i < n; ++i) {
            if (ratings[i] > ratings[i - 1]) {
                candies[i] = candies[i - 1] + 1;
            }
        }

        // Справа налево
        for (int i = n - 2; i >= 0; --i) {
            if (ratings[i] > ratings[i + 1]) {
                candies[i] = max(candies[i], candies[i + 1] + 1);
            }
        }

        int sum = 0;
        for (int c : candies) {
            sum += c;
        }
        return sum;
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