/**
 * https://leetcode.com/problems/integer-to-roman/description/
 */

public class Solution {
    /// <summary>
    /// Преобразует целое число (1 ≤ num ≤ 3999) в римское число.
    ///
    /// Алгоритм:
    /// - Проходим по парам (значение, символ) в порядке убывания.
    /// - Пока num ≥ значение, вычитаем его и добавляем символ в результат.
    /// </summary>
    public string IntToRoman(int num) {
        int[] values = {1000,900,500,400,100,90,50,40,10,9,5,4,1};
        string[] symbols = {"M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"};
        var sb = new System.Text.StringBuilder();
        for (int i = 0; i < values.Length; i++) {
            while (num >= values[i]) {
                num -= values[i];
                sb.Append(symbols[i]);
            }
        }
        return sb.ToString();
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/