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
    /// Находит количество стабильных бинарных массивов.
    /// </summary>
    /// <remarks>
    /// <para><b>Условие:</b> массив должен содержать ровно <c>zero</c> нулей, 
    /// ровно <c>one</c> единиц, и не иметь подмассивов длиной &gt; <c>limit</c>,
    /// состоящих из одинаковых элементов.</para>
    /// 
    /// <para><b>Алгоритм:</b> Динамическое программирование.</para>
    /// 
    /// <para><b>Состояние ДП:</b> <c>dp[i,j,k]</c> — количество стабильных 
    /// массивов с <c>i</c> нулями, <c>j</c> единицами, заканчивающихся битом <c>k</c>.</para>
    /// 
    /// <para><b>Переходы:</b>
    /// <list type="bullet">
    ///   <item>Добавление 0: сумма состояний с (i-1, j) минус недопустимые случаи</item>
    ///   <item>Добавление 1: аналогично с заменой ролей 0 и 1</item>
    /// </list>
    /// </para>
    /// 
    /// <para><b>Сложность:</b> Время: O(zero×one), Память: O(zero×one)</para>
    /// </remarks>
    /// <param name="zero">Требуемое количество нулей</param>
    /// <param name="one">Требуемое количество единиц</param>
    /// <param name="limit">Максимальная длина последовательности одинаковых элементов</param>
    /// <returns>Количество стабильных массивов по модулю 10^9+7</returns>
    public int NumberOfStableArrays(int zero, int one, int limit) {
        const int MOD = 1_000_000_007;
        
        // dp[i,j,k]: i нулей, j единиц, последний бит = k
        var dp = new long[zero + 1, one + 1, 2];
        
        // Базовые случаи: массивы из одного типа элементов
        for (int i = 0; i <= Math.Min(zero, limit); i++)
            dp[i, 0, 0] = 1;
        for (int j = 0; j <= Math.Min(one, limit); j++)
            dp[0, j, 1] = 1;
        
        // Заполнение таблицы ДП
        for (int i = 1; i <= zero; i++) {
            for (int j = 1; j <= one; j++) {
                // Добавляем 0 в конец
                dp[i, j, 0] = (dp[i - 1, j, 0] + dp[i - 1, j, 1] -
                              (i - limit < 1 ? 0 : dp[i - limit - 1, j, 1]) + MOD) % MOD;
                
                // Добавляем 1 в конец
                dp[i, j, 1] = (dp[i, j - 1, 0] + dp[i, j - 1, 1] -
                              (j - limit < 1 ? 0 : dp[i, j - limit - 1, 0]) + MOD) % MOD;
            }
        }
        
        return (int)((dp[zero, one, 0] + dp[zero, one, 1]) % MOD);
    }
}