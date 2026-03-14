/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
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
    long long minNumberOfSeconds(int mountainHeight, vector<int>& workerTimes) {
        auto can = [&](long long T) -> bool {
            long long total = 0;
            for (int w : workerTimes) {
                // d = 1 + 8 * floor(T / w)
                long long d = 1 + 8 * (T / w);
                long long sqrt_d = (long long)sqrtl(d);
                // Корректировка из-за возможной погрешности
                if ((sqrt_d + 1) * (sqrt_d + 1) <= d) sqrt_d++;
                else if (sqrt_d * sqrt_d > d) sqrt_d--;
                long long x = (sqrt_d - 1) / 2;
                total += x;
                if (total >= mountainHeight) return true;
            }
            return total >= mountainHeight;
        };

        long long left = 0, right = 1e18;
        while (left < right) {
            long long mid = left + (right - left) / 2;
            if (can(mid)) right = mid;
            else left = mid + 1;
        }
        return left;
    }
};