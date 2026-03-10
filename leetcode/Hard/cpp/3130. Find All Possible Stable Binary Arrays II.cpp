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
     * @brief Находит количество стабильных бинарных массивов
     * 
     * @param zero Требуемое количество нулей в массиве
     * @param one Требуемое количество единиц в массиве
     * @param limit Максимальная длина подряд идущих одинаковых элементов
     * @return int Количество стабильных массивов по модулю 10^9+7
     * 
     * Алгоритм: Динамическое программирование
     * 
     * Состояние ДП:
     *   dp[i][j][k] — количество стабильных массивов с:
     *     - i нулями
     *     - j единицами  
     *     - последний элемент = k (0 или 1)
     * 
     * Формулы перехода:
     *   - При добавлении 0: dp[i][j][0] = dp[i-1][j][0] + dp[i-1][j][1] 
     *                        - (i > limit ? dp[i-limit-1][j][1] : 0)
     *   - При добавлении 1: аналогично с заменой ролей 0 и 1
     * 
     * Базовые случаи:
     *   - Массивы из одних нулей длиной 1..limit: dp[i][0][0] = 1
     *   - Массивы из одних единиц длиной 1..limit: dp[0][j][1] = 1
     * 
     * Сложность:
     *   Время: O(zero × one)
     *   Память: O(zero × one)
     */
    int numberOfStableArrays(int zero, int one, int limit) {
        constexpr int MOD = 1'000'000'007;
        
        // dp[i][j][k]: i нулей, j единиц, последний бит = k
        vector<vector<vector<long>>> dp(
            zero + 1, 
            vector<vector<long>>(one + 1, vector<long>(2, 0))
        );
        
        // Базовые случаи
        for (int i = 0; i <= min(zero, limit); ++i)
            dp[i][0][0] = 1;
        for (int j = 0; j <= min(one, limit); ++j)
            dp[0][j][1] = 1;
        
        // Заполнение таблицы ДП
        for (int i = 1; i <= zero; ++i) {
            for (int j = 1; j <= one; ++j) {
                // Добавляем 0 в конец
                dp[i][j][0] = (dp[i - 1][j][0] + dp[i - 1][j][1] -
                              (i - limit < 1 ? 0 : dp[i - limit - 1][j][1]) + MOD) % MOD;
                
                // Добавляем 1 в конец
                dp[i][j][1] = (dp[i][j - 1][0] + dp[i][j - 1][1] -
                              (j - limit < 1 ? 0 : dp[i][j - limit - 1][0]) + MOD) % MOD;
            }
        }
        
        return (dp[zero][one][0] + dp[zero][one][1]) % MOD;
    }
};