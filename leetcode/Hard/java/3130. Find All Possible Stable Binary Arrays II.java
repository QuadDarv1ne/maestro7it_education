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
    /**
     * Находит количество стабильных бинарных массивов.
     * 
     * <p><b>Условие стабильности:</b> массив содержит ровно {@code zero} нулей,
     * ровно {@code one} единиц, и ни один подмассив длиной > {@code limit}
     * не состоит из одинаковых элементов.</p>
     * 
     * <p><b>Алгоритм:</b> Динамическое программирование с трёхмерным состоянием.</p>
     * 
     * <p><b>Состояние ДП:</b>
     * <ul>
     *   <li>{@code dp[i][j][k]} — количество стабильных массивов с:
     *     <ul>
     *       <li>{@code i} нулями</li>
     *       <li>{@code j} единицами</li>
     *       <li>последним элементом {@code k} (0 или 1)</li>
     *     </ul>
     *   </li>
     * </ul>
     * 
     * <p><b>Переходы:</b>
     * <ul>
     *   <li>При добавлении 0: {@code dp[i][j][0] = dp[i-1][j][0] + dp[i-1][j][1] 
     *       − (если i > limit: dp[i−limit−1][j][1])}</li>
     *   <li>При добавлении 1: аналогично с заменой 0 ↔ 1</li>
     * </ul>
     * 
     * <p><b>Базовые случаи:</b> массивы из одного типа элементов длиной ≤ limit</p>
     * 
     * <p><b>Сложность:</b> Время: O(zero×one), Память: O(zero×one)</p>
     * 
     * @param zero требуемое количество нулей
     * @param one требуемое количество единиц
     * @param limit максимальная длина подряд идущих одинаковых элементов
     * @return количество стабильных массивов по модулю 10^9+7
     */
    public int numberOfStableArrays(int zero, int one, int limit) {
        final int MOD = 1_000_000_007;
        
        // dp[i][j][k]: i нулей, j единиц, последний бит = k
        long[][][] dp = new long[zero + 1][one + 1][2];
        
        // Базовые случаи
        for (int i = 0; i <= Math.min(zero, limit); ++i)
            dp[i][0][0] = 1;
        for (int j = 0; j <= Math.min(one, limit); ++j)
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
        
        return (int) ((dp[zero][one][0] + dp[zero][one][1]) % MOD);
    }
}