/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

class Solution {
public:
    int largestSubmatrix(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        int maxArea = 0;
        vector<int> heights(n, 0);

        for (int i = 0; i < m; ++i) {
            // Обновляем высоты
            for (int j = 0; j < n; ++j) {
                if (matrix[i][j] == 1) {
                    heights[j]++;
                } else {
                    heights[j] = 0;
                }
            }

            // Копируем и сортируем высоты для текущей строки
            vector<int> sortedHeights = heights;
            sort(sortedHeights.begin(), sortedHeights.end(), greater<int>());

            // Вычисляем максимальную площадь
            for (int j = 0; j < n; ++j) {
                maxArea = max(maxArea, sortedHeights[j] * (j + 1));
            }
        }
        return maxArea;
    }
};