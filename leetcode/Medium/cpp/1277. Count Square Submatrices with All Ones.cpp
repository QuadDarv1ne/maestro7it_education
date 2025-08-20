/**
 * https://leetcode.com/problems/count-square-submatrices-with-all-ones/description/?envType=daily-question&envId=2025-08-20
 */

#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Задача: посчитать количество квадратных подматриц из единиц.
     *
     * Алгоритм:
     * Используем динамическое программирование.
     * dp[i][j] — размер наибольшего квадрата с правым нижним углом в (i, j).
     * Если matrix[i][j] == 1:
     *   dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
     * Итоговый ответ — сумма всех dp[i][j].
     *
     * Сложность:
     *  Время — O(m * n), Память — O(m * n) или O(n) при оптимизации.
     */
    int countSquares(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        int ans = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == 1 && i > 0 && j > 0) {
                    matrix[i][j] = min({matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1]}) + 1;
                }
                ans += matrix[i][j];
            }
        }
        return ans;
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