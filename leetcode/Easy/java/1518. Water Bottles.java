/**
 * https://leetcode.com/problems/water-bottles/description/?envType=daily-question&envId=2025-10-01
 */

class Solution {
    public int numWaterBottles(int numBottles, int numExchange) {
        /*
        Возвращает максимальное число бутылок, которые можно выпить,
        если разрешён обмен numExchange пустых на одну полную.

        Алгоритм:
        1. ans = numBottles, empty = numBottles
        2. Пока empty >= numExchange:
            * newB = empty / numExchange
            * ans += newB
            * empty = empty % numExchange + newB
        3. Вернуть ans
        */
        int ans = numBottles;
        int empty = numBottles;
        while (empty >= numExchange) {
            int newB = empty / numExchange;
            ans += newB;
            empty = (empty % numExchange) + newB;
        }
        return ans;
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