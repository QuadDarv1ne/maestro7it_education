/**
 * https://leetcode.com/problems/reverse-words-in-a-string/description/
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

public class Solution {
    public string ReverseWords(string s) {
        /*
        Разворачивает порядок слов в строке.
        
        Параметры:
        s - строка, которая может содержать лишние пробелы
        
        Возвращает:
        Строку с обратным порядком слов, где слова разделены одним пробелом
        */
        
        // Разбиваем строку на слова, игнорируя пустые записи
        string[] words = s.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        
        // Разворачиваем массив слов
        Array.Reverse(words);
        
        // Объединяем слова через пробел
        return string.Join(" ", words);
    }
}