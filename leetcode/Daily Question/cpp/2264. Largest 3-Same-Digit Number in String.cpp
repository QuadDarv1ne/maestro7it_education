/**
 * https://leetcode.com/problems/largest-3-same-digit-number-in-string/description/?envType=daily-question&envId=2025-08-14
 */

/**
 * @brief Находит наибольшее "хорошее" число в строке.
 * "Хорошее" число — это подстрока из трёх одинаковых цифр.
 *
 * Алгоритм:
 * 1. Перебираем цифры от '9' до '0'.
 * 2. Для каждой цифры создаём строку из трёх одинаковых символов.
 * 3. Если эта строка встречается в num — возвращаем её.
 * 4. Если не найдено — возвращаем пустую строку.
 *
 * Сложность: O(n) по времени, O(1) по памяти.
 */
class Solution {
public:
    string largestGoodInteger(string num) {
        for (char d = '9'; d >= '0'; --d) {
            string t(3, d);
            if (num.find(t) != string::npos) return t;
        }
        return "";
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