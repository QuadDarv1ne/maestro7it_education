/**
 * Подсчёт количества вхождений строки t как подпоследовательности в строку s
 * 
 * @param s Исходная строка, в которой ищем подпоследовательности
 * @param t Строка, которую ищем как подпоследовательность
 * @return Количество различных способов получить t как подпоследовательность s
 * 
 * Сложность: Время O(m×n), Память O(n), где m = s.length(), n = t.length()
 *
 * Алгоритм:
 * 1. dp[j] = количество способов получить префикс t[0..j-1] как подпоследовательность
 * 2. dp[0] = 1 (пустая строка — подпоследовательность любой строки)
 * 3. Для каждого символа s[i] проходим t справа налево
 * 4. Если s[i] == t[j], то dp[j+1] += dp[j]
 * 5. Ответ в dp[n]
 *
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
    int numDistinct(string s, string t) {
        int m = s.length();
        int n = t.length();
        
        // Базовые случаи
        if (m < n) return 0;
        if (n == 0) return 1;
        
        // Используем вектор unsigned long long для больших чисел
        vector<unsigned long long> dp(n + 1, 0);
        dp[0] = 1;  // Пустая подпоследовательность
        
        // Проходим по строке s
        for (int i = 0; i < m; i++) {
            // Проходим по строке t справа налево для избежания перезаписи
            for (int j = n - 1; j >= 0; j--) {
                if (s[i] == t[j]) {
                    dp[j + 1] += dp[j];
                }
            }
        }
        
        return dp[n];
    }
};