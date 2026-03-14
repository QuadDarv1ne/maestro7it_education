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

public class Solution {
    public long MinNumberOfSeconds(int mountainHeight, int[] workerTimes) {
        bool Can(long T) {
            long total = 0;
            foreach (int w in workerTimes) {
                long d = 1 + 8 * (T / w);
                long sqrt_d = (long)Math.Sqrt(d);
                if ((sqrt_d + 1) * (sqrt_d + 1) <= d) sqrt_d++;
                else if (sqrt_d * sqrt_d > d) sqrt_d--;
                long x = (sqrt_d - 1) / 2;
                total += x;
                if (total >= mountainHeight) return true;
            }
            return total >= mountainHeight;
        }

        long left = 0, right = (long)1e18;
        while (left < right) {
            long mid = left + (right - left) / 2;
            if (Can(mid)) right = mid;
            else left = mid + 1;
        }
        return left;
    }
}