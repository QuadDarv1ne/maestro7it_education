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
    /**
     * Проверяет, является ли строка t анаграммой строки s.
     * 
     * Алгоритм (подсчет символов):
     * 1. Если длины строк не равны, возвращаем false.
     * 2. Создаем массив для подсчета частот символов (26 для английских букв).
     * 3. Увеличиваем счетчики для символов строки s.
     * 4. Уменьшаем счетчики для символов строки t.
     * 5. Если все счетчики равны 0, строки являются анаграммами.
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(1) - используем фиксированный массив на 26 элементов
     * 
     * @param s Первая строка
     * @param t Вторая строка
     * @return true, если t является анаграммой s, иначе false
     * 
     * Примеры:
     * IsAnagram("anagram", "nagaram") → true
     * IsAnagram("rat", "car") → false
     * IsAnagram("", "") → true
     */
    public bool IsAnagram(string s, string t) {
        // Если длины строк разные, они не могут быть анаграммами
        if (s.Length != t.Length) {
            return false;
        }
        
        // Массив для подсчета частот символов (26 английских букв)
        int[] charCount = new int[26];
        
        // Увеличиваем счетчики для символов строки s
        foreach (char c in s) {
            charCount[c - 'a']++;
        }
        
        // Уменьшаем счетчики для символов строки t
        foreach (char c in t) {
            int index = c - 'a';
            charCount[index]--;
            // Если счетчик стал отрицательным, значит в t больше этого символа
            if (charCount[index] < 0) {
                return false;
            }
        }
        
        // Все счетчики должны быть равны 0
        foreach (int count in charCount) {
            if (count != 0) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Решение с использованием Dictionary (работает для любого набора символов).
     * 
     * @param s Первая строка
     * @param t Вторая строка
     * @return true, если строки являются анаграммами
     */
    public bool IsAnagramDictionary(string s, string t) {
        if (s.Length != t.Length) {
            return false;
        }
        
        Dictionary<char, int> charCount = new Dictionary<char, int>();
        
        foreach (char c in s) {
            if (charCount.ContainsKey(c)) {
                charCount[c]++;
            } else {
                charCount[c] = 1;
            }
        }
        
        foreach (char c in t) {
            if (!charCount.ContainsKey(c)) {
                return false; // Символ отсутствует в s
            }
            
            charCount[c]--;
            if (charCount[c] < 0) {
                return false;
            }
        }
        
        // Проверяем, что все счетчики равны 0
        foreach (int count in charCount.Values) {
            if (count != 0) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Решение с использованием сортировки.
     * 
     * Сложность:
     * Время: O(n log n)
     * Пространство: O(n) (или O(1) в зависимости от реализации сортировки)
     * 
     * @param s Первая строка
     * @param t Вторая строка
     * @return true, если строки являются анаграммами
     */
    public bool IsAnagramSort(string s, string t) {
        if (s.Length != t.Length) {
            return false;
        }
        
        char[] sArray = s.ToCharArray();
        char[] tArray = t.ToCharArray();
        
        Array.Sort(sArray);
        Array.Sort(tArray);
        
        return new string(sArray) == new string(tArray);
    }
}