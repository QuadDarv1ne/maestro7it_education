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

public class Solution {
    public string ShortestPalindrome(string s) {
        // Алгоритм КМП (Knuth-Morris-Pratt)
        // Находим самый длинный палиндромный префикс строки
        
        if (string.IsNullOrEmpty(s)) {
            return s;
        }
        
        // Создаем обратную строку
        string reversed = ReverseString(s);
        
        // Создаем комбинированную строку: s + "#" + reversed
        string combined = s + "#" + reversed;
        
        // Вычисляем префикс-функцию для комбинированной строки
        int[] pi = ComputePrefixFunction(combined);
        
        // Длина самого длинного палиндромного префикса
        int longestPalindromePrefix = pi[pi.Length - 1];
        
        // Часть, которую нужно добавить в начало
        string toAdd = reversed.Substring(0, s.Length - longestPalindromePrefix);
        
        return toAdd + s;
    }
    
    private string ReverseString(string s) {
        char[] charArray = s.ToCharArray();
        Array.Reverse(charArray);
        return new string(charArray);
    }
    
    private int[] ComputePrefixFunction(string s) {
        int n = s.Length;
        int[] pi = new int[n];
        
        for (int i = 1; i < n; i++) {
            int j = pi[i - 1];
            
            // Пока есть несовпадение, отступаем назад
            while (j > 0 && s[i] != s[j]) {
                j = pi[j - 1];
            }
            
            // Если символы совпадают, увеличиваем j
            if (s[i] == s[j]) {
                j++;
            }
            
            pi[i] = j;
        }
        
        return pi;
    }
}