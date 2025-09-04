/**
 * https://leetcode.com/problems/find-closest-person/description/?envType=daily-question&envId=2025-09-04
 */

class Solution {
    /**
     * Определяет, кто из двух людей ближе к цели.
     *
     * @param x Позиция первого человека
     * @param y Позиция второго человека
     * @param z Позиция цели
     * @return 1, если первый ближе; 
     *         2, если второй ближе; 
     *         0, если оба на одинаковом расстоянии
     */
    public int findClosest(int x, int y, int z) {
        int a = Math.abs(x - z);
        int b = Math.abs(y - z);
        return a == b ? 0 : (a < b ? 1 : 2);
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