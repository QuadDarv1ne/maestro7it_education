/**
 * https://leetcode.com/problems/palindrome-number/description/
 */

/**
 * @brief Определяет, является ли целое x палиндромом, без преобразования в строку.
 *
 * Подход:
 * - Если x < 0 или (x % 10 == 0 && x != 0) → false.
 * - Переворачиваем половину цифр: пока rev < x, делаем rev = rev*10 + x % 10, x /= 10.
 * - В конце сравниваем: rev == x (чётная длина) или rev/10 == x (нечётная длина).
 *
 * Время: O(log₁₀(x)), память: O(1).
 *
 * @param x входное целое
 * @return true, если палиндром, иначе false
 */
class Solution {
public:
    bool isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) return false;
        int rev = 0;
        while (x > rev) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }
        return x == rev || x == rev / 10;
    }
};

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