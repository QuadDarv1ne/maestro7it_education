/**
 * https://leetcode.com/problems/number-of-ways-to-paint-n-3-grid/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Number of Ways to Paint N × 3 Grid"
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
     * Вычисляет количество способов раскрасить сетку N × 3 тремя цветами
     * так, чтобы соседние ячейки (по горизонтали или вертикали) не имели одинаковый цвет.
     * 
     * @param n количество строк в сетке
     * @return количество способов раскраски по модулю 10^9+7
     */
    public int numOfWays(int n) {
        final int MOD = 1000000007;
        
        // Инициализация для первой строки
        long a = 6;  // Строки типа "ABC" (3 разных цвета)
        long b = 6;  // Строки типа "ABA" (первый и третий цвета одинаковы)
        
        // Динамическое программирование для строк 2..n
        for (int i = 2; i <= n; i++) {
            long new_a = (2 * a + 2 * b) % MOD;
            long new_b = (2 * a + 3 * b) % MOD;
            a = new_a;
            b = new_b;
        }
        
        // Общее количество способов
        return (int)((a + b) % MOD);
    }
}