/**
 * https://leetcode.com/problems/count-submatrices-with-all-ones/description/?envType=daily-question&envId=2025-08-21
 */

#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

/**
 * Подсчёт количества подматриц, состоящих только из единиц.
 * @param mat бинарная матрица (vector<vector<int>>)
 * @return количество подматриц (int)
 */
class Solution {
public:
    int numSubmat(vector<vector<int>>& mat) {
        int m = mat.size(), n = mat[0].size();
        vector<vector<int>> continuous(m, vector<int>(n, 0));

        // Подсчёт подряд идущих единиц в строках
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (mat[i][j] == 1) {
                    continuous[i][j] = (j > 0 ? continuous[i][j - 1] : 0) + 1;
                }
            }
        }

        int ans = 0;
        // Подсчёт количества подматриц
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                int minWidth = INT_MAX;
                for (int k = i; k >= 0; k--) {
                    minWidth = min(minWidth, continuous[k][j]);
                    ans += minWidth;
                }
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