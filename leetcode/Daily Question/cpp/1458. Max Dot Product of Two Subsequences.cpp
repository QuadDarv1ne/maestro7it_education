/**
 * Максимальное скалярное произведение двух подпоследовательностей
 * 
 * @param nums1 Первый массив целых чисел
 * @param nums2 Второй массив целых чисел
 * @return Максимальное скалярное произведение
 * 
 * Сложность: Время O(m*n), Память O(m*n)
 *
 * Автор: Дуплей Максим Игоревич
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
    int maxDotProduct(vector<int>& nums1, vector<int>& nums2) {
        int m = nums1.size();
        int n = nums2.size();
        
        // DP таблица с инициализацией минимальным значением
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, INT_MIN / 2));
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                int product = nums1[i - 1] * nums2[j - 1];
                
                // Выбираем лучший из 4 вариантов:
                // 1. Только текущее произведение
                // 2. Добавить к предыдущей подпоследовательности
                // 3. Пропустить элемент nums1
                // 4. Пропустить элемент nums2
                dp[i][j] = max({
                    product,
                    dp[i - 1][j - 1] + product,
                    dp[i - 1][j],
                    dp[i][j - 1]
                });
            }
        }
        
        return dp[m][n];
    }
};