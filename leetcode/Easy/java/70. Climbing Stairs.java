/**
 * https://leetcode.com/problems/climbing-stairs/description/?envType=study-plan-v2&envId=top-interview-150
 */

class Solution {
    /**
     * Считает количество способов подняться на лестницу из n ступеней,
     * делая за раз 1 или 2 шага.
     *
     * Алгоритм:
     * Используется улучшенное DP в духе Фибоначчи:
     * ways[n] = ways[n-1] + ways[n-2], храня только два предыдущих значения.
     *
     * @param n — количество ступеней
     * @return — число способов
     * Время: O(n), Память: O(1)
     */
    public int climbStairs(int n) {
        if (n <= 1) return 1;
        int first = 1;
        int second = 2;
        for (int i = 3; i <= n; i++) {
            int third = first + second;
            first = second;
            second = third;
        }
        return second;
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