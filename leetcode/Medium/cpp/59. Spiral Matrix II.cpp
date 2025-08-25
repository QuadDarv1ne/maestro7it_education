/**
 * https://leetcode.com/problems/spiral-matrix-ii/description/
 */

#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Генерация матрицы n x n по спирали
     */
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> matrix(n, vector<int>(n, 0));
        int left = 0, right = n - 1;
        int top = 0, bottom = n - 1;
        int num = 1;

        while (left <= right && top <= bottom) {
            // Верхняя строка
            for (int j = left; j <= right; j++) matrix[top][j] = num++;
            top++;

            // Правый столбец
            for (int i = top; i <= bottom; i++) matrix[i][right] = num++;
            right--;

            // Нижняя строка
            if (top <= bottom) {
                for (int j = right; j >= left; j--) matrix[bottom][j] = num++;
                bottom--;
            }

            // Левый столбец
            if (left <= right) {
                for (int i = bottom; i >= top; i--) matrix[i][left] = num++;
                left++;
            }
        }

        return matrix;
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