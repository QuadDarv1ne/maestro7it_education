/**
 * https://leetcode.com/problems/palindrome-number/description/
 */

/// <summary>
/// Проверяет, является ли число палиндромом без преобразования в строку.
/// </summary>
/// <param name="x">Входное значение</param>
/// <returns>true, если палиндром, иначе false</returns>
/// <remarks>
/// Алгоритм:
/// - Отрицательные числа и числа, заканчивающиеся на 0 (кроме 0) → false.
/// - Переворачиваем вторую половину цифр:
///     rev = rev*10 + x % 10; x /= 10;
///     продолжаем пока x > rev.
/// - Сравниваем: x == rev (чётная длина) или x == rev/10 (нечётная).
/// Время: O(log₁₀(x)), память: O(1).
/// </remarks>
public class Solution {
    public bool IsPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) return false;
        int rev = 0;
        while (x > rev) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }
        return x == rev || x == rev / 10;
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