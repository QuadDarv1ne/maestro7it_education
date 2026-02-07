/**
 * https://leetcode.com/problems/shortest-palindrome/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "214. Shortest Palindrome"
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
    string shortestPalindrome(string s) {
        // Используем алгоритм КМП
        string rev_s = s;
        reverse(rev_s.begin(), rev_s.end());
        
        // Создаем комбинированную строку
        string combined = s + "#" + rev_s;
        
        // Вычисляем префикс-функцию
        int n = combined.length();
        vector<int> pi(n, 0);
        
        for (int i = 1; i < n; i++) {
            int j = pi[i - 1];
            
            while (j > 0 && combined[i] != combined[j]) {
                j = pi[j - 1];
            }
            
            if (combined[i] == combined[j]) {
                j++;
            }
            
            pi[i] = j;
        }
        
        // Длина самого длинного палиндромного префикса
        int longest = pi[n - 1];
        
        // Часть для добавления в начало
        string to_add = rev_s.substr(0, s.length() - longest);
        
        return to_add + s;
    }
};