/**
 * https://leetcode.com/problems/convert-integer-to-the-sum-of-two-no-zero-integers/description/?envType=daily-question&envId=2025-09-08
 */

class Solution {
public:
    /**
     * Задача: Разбить число n на два положительных числа a и b,
     * такие что:
     * 1) a + b = n
     * 2) a и b не содержат цифру '0'
     *
     * Метод:
     * - Перебираем числа a от 1 до n-1
     * - Вычисляем b = n - a
     * - Проверяем, что a и b не содержат '0'
     * - Возвращаем первую подходящую пару
     */
    vector<int> getNoZeroIntegers(int n) {
        for (int a = 1; a < n; ++a) {
            int b = n - a;
            if (to_string(a).find('0') == string::npos &&
                to_string(b).find('0') == string::npos) {
                return {a, b};
            }
        }
        return {};
    }
};

/*
''' Полезные ссылки: '''
# 1. Telegram❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/