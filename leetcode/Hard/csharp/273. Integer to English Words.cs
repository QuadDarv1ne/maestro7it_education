/**
 * https://leetcode.com/problems/basic-calculator/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "224. Basic Calculator"
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
    public string NumberToWords(int num) {
        /**
         * Преобразует целое число в английские слова.
         * 
         * @param num Число от 0 до 2 147 483 647
         * @return Строковое представление с заглавной буквы
         * 
         * Примеры:
         *   NumberToWords(123) → "One Hundred Twenty Three"
         *   NumberToWords(1000010) → "One Million Ten"
         * 
         * Особенности:
         *   - Использует рекурсию для обработки групп
         *   - Учитывает пробелы и форматирование
         */
        if (num == 0) return "Zero";
        
        string[] ones = {"", "One", "Two", "Three", "Four", "Five", "Six", "Seven", 
                        "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", 
                        "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"};
        string[] tens = {"", "", "Twenty", "Thirty", "Forty", "Fifty", 
                        "Sixty", "Seventy", "Eighty", "Ninety"};
        string[] thousands = {"", "Thousand", "Million", "Billion"};
        
        string Helper(int n) {
            if (n == 0) return "";
            if (n < 20) return ones[n] + " ";
            if (n < 100) return tens[n / 10] + " " + Helper(n % 10);
            return ones[n / 100] + " Hundred " + Helper(n % 100);
        }
        
        string result = "";
        int i = 0;
        
        while (num > 0) {
            if (num % 1000 != 0) {
                string group = Helper(num % 1000).Trim();
                result = group + " " + thousands[i] + " " + result;
            }
            num /= 1000;
            i++;
        }
        
        return result.Trim();
    }
}