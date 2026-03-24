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
 * 
 * Находит максимальное неотрицательное произведение на пути из (0,0) в (m-1,n-1).
 * 
 * Параметры:
 *     grid - матрица целых чисел размером m x n
 * 
 * Возвращает:
 *     максимальное неотрицательное произведение по модулю 10^9+7,
 *     или -1, если такого произведения нет
 * 
 * Примечания:
 *     - Движение возможно только вправо или вниз
 *     - Отрицательные числа могут менять знак произведения
 *     - Используется динамическое программирование с отслеживанием
 *       максимального и минимального произведения в каждой ячейке
 *     - Сложность: O(m*n) по времени и O(m*n) по памяти
 */

class Solution {
public:
    int maxProductPath(vector<vector<int>>& grid) {
        const int MOD = 1e9 + 7;
        int m = grid.size(), n = grid[0].size();
        
        // Используем long long для избежания переполнения
        vector<vector<long long>> maxDP(m, vector<long long>(n));
        vector<vector<long long>> minDP(m, vector<long long>(n));
        
        // Инициализация начальной ячейки
        maxDP[0][0] = minDP[0][0] = grid[0][0];
        
        // Заполняем первую строку
        for (int j = 1; j < n; ++j) {
            maxDP[0][j] = minDP[0][j] = maxDP[0][j-1] * grid[0][j];
        }
        
        // Заполняем первый столбец
        for (int i = 1; i < m; ++i) {
            maxDP[i][0] = minDP[i][0] = maxDP[i-1][0] * grid[i][0];
        }
        
        // Основной DP
        for (int i = 1; i < m; ++i) {
            for (int j = 1; j < n; ++j) {
                long long curr = grid[i][j];
                vector<long long> candidates = {
                    maxDP[i-1][j] * curr,
                    minDP[i-1][j] * curr,
                    maxDP[i][j-1] * curr,
                    minDP[i][j-1] * curr
                };
                maxDP[i][j] = *max_element(candidates.begin(), candidates.end());
                minDP[i][j] = *min_element(candidates.begin(), candidates.end());
            }
        }
        
        long long result = maxDP[m-1][n-1];
        if (result < 0) return -1;
        return result % MOD;
    }
};