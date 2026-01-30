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

class Solution {
public:
    string reverseWords(string s) {
        /*
        Разворачивает порядок слов в строке.
        
        Параметры:
        s - строка, которая может содержать лишние пробелы
        
        Возвращает:
        Строку с обратным порядком слов, где слова разделены одним пробелом
        
        Алгоритм:
        - Используем два указателя для обработки строки с конца
        - Пропускаем пробелы и находим границы слов
        - Добавляем слова в результирующую строку
        */
        
        string result = "";
        int i = s.length() - 1;
        
        while (i >= 0) {
            // Пропускаем пробелы с конца
            while (i >= 0 && s[i] == ' ') {
                i--;
            }
            
            if (i < 0) {
                break;
            }
            
            int j = i;
            // Находим начало слова
            while (j >= 0 && s[j] != ' ') {
                j--;
            }
            
            // Извлекаем слово и добавляем в результат
            if (!result.empty()) {
                result += " ";
            }
            result += s.substr(j + 1, i - j);
            
            // Переходим к следующему слову
            i = j - 1;
        }
        
        return result;
    }
};