/**
 * https://leetcode.com/problems/maximum-average-pass-ratio/description/?envType=daily-question&envId=2025-09-01
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Возвращает максимальную среднюю долю сдавших после распределения extraStudents.
    /// </summary>
    public double MaxAverageRatio(int[][] classes, int extraStudents) {
        // priority = -gain, потому что PriorityQueue извлекает минимальную priority,
        // а нам нужен максимум gain.
        var pq = new PriorityQueue<(int p, int t), double>();

        foreach (var c in classes) {
            int p = c[0], t = c[1];
            pq.Enqueue((p, t), -Gain(p, t));
        }

        while (extraStudents-- > 0) {
            var cur = pq.Dequeue();
            int p = cur.Item1 + 1;
            int t = cur.Item2 + 1;
            pq.Enqueue((p, t), -Gain(p, t));
        }

        double sum = 0.0;
        while (pq.Count > 0) {
            var cur = pq.Dequeue();
            sum += (double)cur.Item1 / cur.Item2;
        }

        return sum / classes.Length;
    }

    private double Gain(int p, int t) {
        return (double)(p + 1) / (t + 1) - (double)p / t;
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