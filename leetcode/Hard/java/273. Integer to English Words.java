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
     * Алгоритмическая сложность:
     *   Время: O(log₁₀ n) — обрабатываем каждую группу из 3 цифр
     *   Память: O(1) — фиксированные массивы слов
     */
    public String numberToWords(int num) {
        if (num == 0) return "Zero";
        
        String[] ones = {"", "One", "Two", "Three", "Four", "Five", "Six", "Seven", 
                        "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", 
                        "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"};
        String[] tens = {"", "", "Twenty", "Thirty", "Forty", "Fifty", 
                        "Sixty", "Seventy", "Eighty", "Ninety"};
        String[] thousands = {"", "Thousand", "Million", "Billion"};
        
        StringBuilder result = new StringBuilder();
        int i = 0;
        
        while (num > 0) {
            if (num % 1000 != 0) {
                StringBuilder group = new StringBuilder();
                helper(num % 1000, ones, tens, group);
                result.insert(0, group.toString() + thousands[i] + " ");
            }
            num /= 1000;
            i++;
        }
        
        return result.toString().trim();
    }
    
    private void helper(int n, String[] ones, String[] tens, StringBuilder sb) {
        if (n == 0) return;
        if (n < 20) {
            sb.append(ones[n]).append(" ");
        } else if (n < 100) {
            sb.append(tens[n / 10]).append(" ");
            helper(n % 10, ones, tens, sb);
        } else {
            sb.append(ones[n / 100]).append(" Hundred ");
            helper(n % 100, ones, tens, sb);
        }
    }
}