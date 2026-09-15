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

public class Solution {
    /// <summary>
    /// Находит максимальный счет и количество путей с этим счетом.
    /// 
    /// Игрок начинает с позиции (n-1, n-1) и движется вверх, влево или по диагонали
    /// к позиции (0, 0). Цифры на пути добавляются к счету. Символы 'E' и 'S' 
    /// не добавляют очков. Препятствия 'X' блокируют путь.
    /// </summary>
    /// <param name="board">Массив строк, представляющих игровое поле</param>
    /// <returns>Массив из двух чисел [max_score, count]:
    /// - max_score: максимально возможный счет, или 0 если пути нет
    /// - count: количество путей с максимальным счетом по модулю 10^9+7</returns>
    public int[] PathsWithMaxScore(IList<string> board) {
        const int MOD = 1000000007;
        int n = board.Count;
        
        // dp[i][j] = [max_score, count]
        int[][][] dp = new int[n][][];
        for (int i = 0; i < n; i++) {
            dp[i] = new int[n][];
            for (int j = 0; j < n; j++) {
                dp[i][j] = new int[] { -1, 0 };
            }
        }
        
        // Начальная позиция
        dp[n-1][n-1][0] = 0;
        dp[n-1][n-1][1] = 1;
        
        // Возможные направления: вниз, вправо, диагональ
        int[][] directions = new int[][] {
            new int[] { 1, 0 },
            new int[] { 0, 1 },
            new int[] { 1, 1 }
        };
        
        // Заполняем dp снизу вверх и справа налево
        for (int i = n - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                if (board[i][j] == 'X' || (i == n-1 && j == n-1)) {
                    continue;
                }
                
                int maxScore = -1;
                int count = 0;
                
                // Проверяем три возможных направления
                foreach (var dir in directions) {
                    int ni = i + dir[0];
                    int nj = j + dir[1];
                    
                    if (ni < n && nj < n && dp[ni][nj][0] != -1) {
                        int score = dp[ni][nj][0];
                        if (score > maxScore) {
                            maxScore = score;
                            count = dp[ni][nj][1];
                        } else if (score == maxScore) {
                            count = (count + dp[ni][nj][1]) % MOD;
                        }
                    }
                }
                
                if (maxScore != -1) {
                    // Добавляем очки текущей клетки (если это не 'E' и не 'S')
                    if (board[i][j] != 'E' && board[i][j] != 'S') {
                        maxScore += (board[i][j] - '0');
                    }
                    dp[i][j][0] = maxScore;
                    dp[i][j][1] = count;
                }
            }
        }
        
        if (dp[0][0][0] == -1) {
            return new int[] { 0, 0 };
        }
        return new int[] { dp[0][0][0], dp[0][0][1] };
    }
}