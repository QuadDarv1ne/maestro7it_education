/**
 * https://leetcode.com/problems/largest-3-same-digit-number-in-string/description/?envType=daily-question&envId=2025-08-14
 */

/**
 * Находит наибольшее "хорошее" число в строке.
 * "Хорошее" число — это подстрока длиной 3, где все символы одинаковы.
 *
 * Алгоритм:
 * 1. Цикл от '9' до '0'.
 * 2. Строим строку из трёх одинаковых символов.
 * 3. Проверяем, содержится ли она в num.
 * 4. Первое совпадение — ответ.
 *
 * Сложность: O(n) по времени, O(1) по памяти.
 */
class Solution {
    public String largestGoodInteger(String num) {
        for (char d = '9'; d >= '0'; --d) {
            String t = String.valueOf(d).repeat(3);
            if (num.contains(t)) {
                return t;
            }
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