/*
https://leetcode.com/problems/divide-two-integers/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public int Divide(int dividend, int divisor) {
        const int INT_MAX = 2147483647;
        const int INT_MIN = -2147483648;

        if (dividend == INT_MIN && divisor == -1)
            return INT_MAX;

        bool negative = (dividend < 0) ^ (divisor < 0);

        long dvd = Math.Abs((long)dividend);
        long dvs = Math.Abs((long)divisor);
        long quotient = 0;

        while (dvd >= dvs) {
            long temp = dvs, multiple = 1;
            while (dvd >= (temp << 1)) {
                temp <<= 1;
                multiple <<= 1;
            }
            dvd -= temp;
            quotient += multiple;
        }

        quotient = negative ? -quotient : quotient;
        if (quotient > INT_MAX) quotient = INT_MAX;
        if (quotient < INT_MIN) quotient = INT_MIN;

        return (int)quotient;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/