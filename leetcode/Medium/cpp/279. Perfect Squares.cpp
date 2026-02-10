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
    int numSquares(int n) {
        /**
         * Находит минимальное количество полных квадратов, дающих в сумме n.
         * 
         * @param n Целое положительное число
         * @return Минимальное количество квадратов
         * 
         * @example numSquares(12) → 3  // 4 + 4 + 4
         * @example numSquares(13) → 2  // 4 + 9
         * 
         * Сложность:
         *   Время: O(n * √n)
         *   Память: O(n)
         */
        vector<int> dp(n + 1, INT_MAX);
        dp[0] = 0;  // Базовый случай
        
        // Генерируем все квадраты, не превышающие n
        vector<int> squares;
        for (int i = 1; i * i <= n; i++) {
            squares.push_back(i * i);
        }
        
        for (int i = 1; i <= n; i++) {
            for (int square : squares) {
                if (square > i) break;
                dp[i] = min(dp[i], dp[i - square] + 1);
            }
        }
        
        return dp[n];
    }
};