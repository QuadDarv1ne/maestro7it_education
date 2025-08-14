/**
 * https://leetcode.com/problems/largest-3-same-digit-number-in-string/description/?envType=daily-question&envId=2025-08-14
 */

/// <summary>
/// Находит наибольшее "хорошее" число в строке.
/// "Хорошее" число — это подстрока из трёх одинаковых цифр.
/// </summary>
/// <param name="num">Входная строка, содержащая только цифры.</param>
/// <returns>Наибольшее "хорошее" число или пустая строка.</returns>
/// <remarks>
/// Алгоритм:
/// 1. Перебор от '9' до '0'.
/// 2. Формируем строку из трёх одинаковых символов.
/// 3. Проверяем, есть ли она в num.
/// </remarks>
public class Solution {
    public string LargestGoodInteger(string num) {
        for (char d = '9'; d >= '0'; d--) {
            string t = new string(d, 3);
            if (num.Contains(t)) return t;
        }
        return "";
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