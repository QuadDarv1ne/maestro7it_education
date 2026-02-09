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

import java.util.Arrays;
import java.util.HashMap;

class Solution {
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
    public boolean isAnagram(String s, String t) {
        // Если длины строк разные, они не могут быть анаграммами
        if (s.length() != t.length()) {
            return false;
        }
        
        // Массив для подсчета частот символов (26 английских букв)
        int[] charCount = new int[26];
        
        // Увеличиваем счетчики для символов строки s
        for (int i = 0; i < s.length(); i++) {
            charCount[s.charAt(i) - 'a']++;
        }
        
        // Уменьшаем счетчики для символов строки t
        for (int i = 0; i < t.length(); i++) {
            int index = t.charAt(i) - 'a';
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
     * Решение с использованием HashMap (работает для любого набора символов).
     * 
     * @param s Первая строка
     * @param t Вторая строка
     * @return true, если строки являются анаграммами
     */
    public boolean isAnagramHashMap(String s, String t) {
        if (s.length() != t.length()) {
            return false;
        }
        
        HashMap<Character, Integer> charCount = new HashMap<>();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            charCount.put(c, charCount.getOrDefault(c, 0) + 1);
        }
        
        for (int i = 0; i < t.length(); i++) {
            char c = t.charAt(i);
            charCount.put(c, charCount.getOrDefault(c, 0) - 1);
            if (charCount.get(c) < 0) {
                return false;
            }
        }
        
        // Проверяем, что все счетчики равны 0
        for (int count : charCount.values()) {
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
    public boolean isAnagramSort(String s, String t) {
        if (s.length() != t.length()) {
            return false;
        }
        
        char[] sArray = s.toCharArray();
        char[] tArray = t.toCharArray();
        
        Arrays.sort(sArray);
        Arrays.sort(tArray);
        
        return Arrays.equals(sArray, tArray);
    }
}