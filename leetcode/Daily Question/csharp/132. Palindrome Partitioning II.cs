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
    public int MinCut(string s) {
        /**
         * Находит минимальное количество разрезов для разбиения строки на палиндромы.
         * 
         * Алгоритм:
         * 1. Создаем матрицу для проверки палиндромов
         * 2. Используем динамическое программирование для нахождения минимальных разрезов
         * 
         * Сложность: O(n²) время, O(n²) память
         */
        
        int n = s.Length;
        if (n <= 1) return 0;
        
        // 1. Матрица для проверки палиндромов
        bool[,] isPalindrome = new bool[n, n];
        
        // Все подстроки длины 1 - палиндромы
        for (int i = 0; i < n; i++) {
            isPalindrome[i, i] = true;
        }
        
        // Проверяем подстроки длины 2 и больше
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i <= n - length; i++) {
                int j = i + length - 1;
                
                if (length == 2) {
                    isPalindrome[i, j] = (s[i] == s[j]);
                } else {
                    isPalindrome[i, j] = (s[i] == s[j] && isPalindrome[i + 1, j - 1]);
                }
            }
        }
        
        // 2. Динамическое программирование для минимальных разрезов
        int[] minCuts = new int[n + 1];
        for (int i = 0; i <= n; i++) {
            minCuts[i] = int.MaxValue;
        }
        minCuts[0] = -1; // Для пустой строки
        
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                // Если s.Substring(j, i - j) - палиндром
                if (isPalindrome[j, i - 1]) {
                    if (minCuts[j] + 1 < minCuts[i]) {
                        minCuts[i] = minCuts[j] + 1;
                    }
                }
            }
        }
        
        return minCuts[n];
    }
}