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
    public String reverseWords(String s) {
        /*
        Разворачивает порядок слов в строке.
        
        Параметры:
        s - строка, которая может содержать лишние пробелы
        
        Возвращает:
        Строку с обратным порядком слов, где слова разделены одним пробелом
        
        Алгоритм:
        - Удаляем лишние пробелы с помощью trim() и split()
        - Собираем слова в обратном порядке через StringBuilder
        */
        
        // Удаляем пробелы по краям и разбиваем на слова
        String[] words = s.trim().split("\\s+");
        
        // Создаем StringBuilder для эффективной конкатенации
        StringBuilder result = new StringBuilder();
        
        // Добавляем слова в обратном порядке
        for (int i = words.length - 1; i >= 0; i--) {
            result.append(words[i]);
            if (i > 0) {
                result.append(" ");
            }
        }
        
        return result.toString();
    }
}