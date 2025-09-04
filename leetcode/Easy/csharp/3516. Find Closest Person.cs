/**
 * https://leetcode.com/problems/find-closest-person/description/?envType=daily-question&envId=2025-09-04
 */

public class Solution {
    /// <summary>
    /// Определяет, кто из двух людей ближе к цели.
    /// Возвращает:
    /// 1 — если первый человек ближе,
    /// 2 — если второй человек ближе,
    /// 0 — если оба на одинаковом расстоянии.
    /// </summary>
    public int FindClosest(int x, int y, int z) {
        int a = Math.Abs(x - z);
        int b = Math.Abs(y - z);
        if (a == b) return 0;
        return a < b ? 1 : 2;
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