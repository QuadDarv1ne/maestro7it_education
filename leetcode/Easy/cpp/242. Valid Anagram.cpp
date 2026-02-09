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

#include <string>
#include <vector>
#include <algorithm>
#include <unordered_map>
using namespace std;

class Solution {
public:
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
     * isAnagram("anagram", "nagaram") → true
     * isAnagram("rat", "car") → false
     * isAnagram("", "") → true
     */
    bool isAnagram(string s, string t) {
        // Если длины строк разные, они не могут быть анаграммами
        if (s.length() != t.length()) {
            return false;
        }
        
        // Массив для подсчета частот символов (26 английских букв)
        vector<int> charCount(26, 0);
        
        // Увеличиваем счетчики для символов строки s
        for (char c : s) {
            charCount[c - 'a']++;
        }
        
        // Уменьшаем счетчики для символов строки t
        for (char c : t) {
            int index = c - 'a';
            charCount[index]--;
            // Если счетчик стал отрицательным, значит в t больше этого символа
            if (charCount[index] < 0) {
                return false;
            }
        }
        
        // Все счетчики должны быть равны 0
        for (int count : charCount) {
            if (count != 0) {
                return false;
            }
        }
        
        return true;
    }
    
    /**
     * Решение с использованием unordered_map (работает для любого набора символов).
     * 
     * @param s Первая строка
     * @param t Вторая строка
     * @return true, если строки являются анаграммами
     */
    bool isAnagramHashMap(string s, string t) {
        if (s.length() != t.length()) {
            return false;
        }
        
        unordered_map<char, int> charCount;
        
        for (char c : s) {
            charCount[c]++;
        }
        
        for (char c : t) {
            charCount[c]--;
            if (charCount[c] < 0) {
                return false;
            }
        }
        
        // Проверяем, что все счетчики равны 0
        for (auto& pair : charCount) {
            if (pair.second != 0) {
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
     * Пространство: O(1) или O(n) в зависимости от реализации сортировки
     * 
     * @param s Первая строка
     * @param t Вторая строка
     * @return true, если строки являются анаграммами
     */
    bool isAnagramSort(string s, string t) {
        if (s.length() != t.length()) {
            return false;
        }
        
        sort(s.begin(), s.end());
        sort(t.begin(), t.end());
        
        return s == t;
    }
};