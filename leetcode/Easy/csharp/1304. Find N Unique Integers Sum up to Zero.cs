/**
 * https://leetcode.com/problems/find-n-unique-integers-sum-up-to-zero/description/?envType=daily-question&envId=2025-09-07
 */

public class Solution {
    /// <summary>
    /// Возвращает массив из n уникальных целых чис с суммой 0.
    /// Если n нечётное — добавляется 0, затем пары (i, -i).
    /// </summary>
    public int[] SumZero(int n) {
        int[] answer = new int[n];
        int index = 0;
        if (n % 2 == 1)
            answer[index++] = 0;
        n /= 2;
        for (int i = 1; i <= n; i++) {
            answer[index++] = i;
            answer[index++] = -i;
        }
        return answer;
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