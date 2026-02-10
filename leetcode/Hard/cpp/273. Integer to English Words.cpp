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

class Solution {
public:
    string numberToWords(int num) {
        /**
         * Преобразует целое число в английские слова.
         * 
         * @param num Число от 0 до 2^31-1
         * @return Строковое представление с заглавной буквы
         * 
         * Примеры:
         *   numberToWords(123) → "One Hundred Twenty Three"
         *   numberToWords(1234567) → "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
         * 
         * Алгоритм:
         *   1. Обработка нуля
         *   2. Рекурсивная обработка групп по 3 цифры
         *   3. Использование статических массивов для базовых слов
         */
        if (num == 0) return "Zero";
        
        vector<string> ones = {"", "One", "Two", "Three", "Four", "Five", "Six", "Seven", 
                               "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", 
                               "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"};
        vector<string> tens = {"", "", "Twenty", "Thirty", "Forty", "Fifty", 
                               "Sixty", "Seventy", "Eighty", "Ninety"};
        vector<string> thousands = {"", "Thousand", "Million", "Billion"};
        
        function<string(int)> helper = [&](int n) -> string {
            if (n == 0) return "";
            else if (n < 20) return ones[n] + " ";
            else if (n < 100) return tens[n / 10] + " " + helper(n % 10);
            else return ones[n / 100] + " Hundred " + helper(n % 100);
        };
        
        string result;
        int i = 0;
        
        while (num > 0) {
            if (num % 1000 != 0) {
                string group = helper(num % 1000);
                result = group + thousands[i] + " " + result;
            }
            num /= 1000;
            i++;
        }
        
        // Удаляем лишние пробелы
        while (!result.empty() && result.back() == ' ') result.pop_back();
        return result;
    }
};