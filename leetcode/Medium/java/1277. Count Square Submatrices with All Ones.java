/**
 * https://leetcode.com/problems/count-square-submatrices-with-all-ones/description/?envType=daily-question&envId=2025-08-20
 */

class Solution {
    /**
     * Задача: посчитать количество квадратных подматриц,
     * содержащих только единицы.
     *
     * Алгоритм:
     * Для каждой ячейки (i, j) считаем dp[i][j] —
     * размер наибольшего квадрата, оканчивающегося в этой точке.
     * Если matrix[i][j] == 1:
     *   dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
     * Результат — сумма всех dp[i][j].
     *
     * Сложность:
     *   O(m * n) по времени и O(1) дополнительной памяти (если обновлять матрицу).
     */
    public int countSquares(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int ans = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == 1 && i > 0 && j > 0) {
                    matrix[i][j] = Math.min(
                        Math.min(matrix[i-1][j], matrix[i][j-1]),
                        matrix[i-1][j-1]
                    ) + 1;
                }
                ans += matrix[i][j];
            }
        }
        return ans;
    }
}

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