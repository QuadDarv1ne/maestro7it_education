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
    /**
     * Вычисляет минимальное начальное здоровье рыцаря для спасения принцессы.
     * Использует обратное динамическое программирование (от конца к началу).
     * 
     * Сложность по времени: O(m * n)
     * Сложность по памяти: O(m * n)
     */
    int calculateMinimumHP(vector<vector<int>>& dungeon) {
        int m = dungeon.size();
        int n = dungeon[0].size();
        
        // Создаём DP таблицу с дополнительной строкой и столбцом
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, INT_MAX));
        
        // Базовые случаи
        dp[m - 1][n] = 1;
        dp[m][n - 1] = 1;
        
        // Заполняем таблицу от конца к началу
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                // Минимальное HP нужное для следующего хода
                int minHpNext = min(dp[i + 1][j], dp[i][j + 1]);
                
                // HP нужное для текущей клетки
                dp[i][j] = max(1, minHpNext - dungeon[i][j]);
            }
        }
        
        return dp[0][0];
    }
};