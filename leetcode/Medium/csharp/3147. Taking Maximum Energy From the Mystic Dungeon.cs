/**
 * https://leetcode.com/problems/taking-maximum-energy-from-the-mystic-dungeon/description/?envType=daily-question&envId=2025-10-10
 */

public class Solution {
    public int MaximumEnergy(int[] energy, int k) {
        // Вычисляет максимальную энергию, которую можно получить,
        // начиная с некоторого мага и прыгая через k шагов каждый раз.
        // Используется динамическое программирование:
        // dp[i] = energy[i] + dp[i + k] (если индекс в пределах массива).
        // Возвращается максимальное значение dp[i].

        int n = energy.Length;
        int[] dp = new int[n];
        int ans = int.MinValue;

        for (int i = n - 1; i >= 0; i--) {
            dp[i] = energy[i];
            int j = i + k;
            if (j < n) {
                dp[i] += dp[j];
            }
            if (dp[i] > ans)
                ans = dp[i];
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