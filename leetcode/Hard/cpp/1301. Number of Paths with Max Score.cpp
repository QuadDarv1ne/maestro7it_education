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
     * Находит максимальный счет и количество путей с этим счетом.
     * 
     * Игрок начинает с позиции (n-1, n-1) и движется вверх, влево или по диагонали
     * к позиции (0, 0). Цифры на пути добавляются к счету. Символы 'E' и 'S' 
     * не добавляют очков. Препятствия 'X' блокируют путь.
     * 
     * @param board вектор строк, представляющих игровое поле
     * @return вектор из двух чисел [max_score, count]:
     *         - max_score: максимально возможный счет, или 0 если пути нет
     *         - count: количество путей с максимальным счетом по модулю 10^9+7
     */
    vector<int> pathsWithMaxScore(vector<string>& board) {
        const int MOD = 1e9 + 7;
        int n = board.size();
        
        // dp[i][j] = {max_score, count}
        vector<vector<pair<int, int>>> dp(n, vector<pair<int, int>>(n, {-1, 0}));
        
        // Начальная позиция
        dp[n-1][n-1] = {0, 1};
        
        // Возможные направления: вниз, вправо, диагональ
        vector<pair<int, int>> directions = {{1, 0}, {0, 1}, {1, 1}};
        
        // Заполняем dp снизу вверх и справа налево
        for (int i = n - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                if (board[i][j] == 'X' || (i == n-1 && j == n-1)) {
                    continue;
                }
                
                int max_score = -1;
                int count = 0;
                
                // Проверяем три возможных направления
                for (auto& dir : directions) {
                    int ni = i + dir.first;
                    int nj = j + dir.second;
                    
                    if (ni < n && nj < n && dp[ni][nj].first != -1) {
                        int score = dp[ni][nj].first;
                        if (score > max_score) {
                            max_score = score;
                            count = dp[ni][nj].second;
                        } else if (score == max_score) {
                            count = (count + dp[ni][nj].second) % MOD;
                        }
                    }
                }
                
                if (max_score != -1) {
                    // Добавляем очки текущей клетки (если это не 'E' и не 'S')
                    if (board[i][j] != 'E' && board[i][j] != 'S') {
                        max_score += (board[i][j] - '0');
                    }
                    dp[i][j] = {max_score, count};
                }
            }
        }
        
        if (dp[0][0].first == -1) {
            return {0, 0};
        }
        return {dp[0][0].first, dp[0][0].second};
    }
};