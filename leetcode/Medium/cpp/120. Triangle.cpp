/**
 * https://leetcode.com/problems/triangle/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <vector>
#include <algorithm>

class Solution {
public:
    /**
     * Находит минимальную сумму пути от вершины треугольника до основания.
     * Двигаемся по соседним числам на каждом уровне, используя динамическое программирование.
     *
     * @param triangle Вектор векторов целых чисел, представляющих треугольник.
     * @return Минимальная сумма пути.
     */
    int minimumTotal(std::vector<std::vector<int>>& triangle) {
        std::vector<int> dp = triangle.back();  // Копируем последний уровень
        
        for (int row = (int)triangle.size() - 2; row >= 0; --row) {
            for (int i = 0; i < (int)triangle[row].size(); ++i) {
                dp[i] = triangle[row][i] + std::min(dp[i], dp[i + 1]);
            }
        }
        
        return dp[0];
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