/**
 * https://leetcode.com/problems/find-the-maximum-number-of-fruits-collected/description/?envType=daily-question&envId=2025-08-16
 */

/// <summary>
/// Задача: Найти максимальное количество фруктов, которое можно собрать.
/// fruits[i] = [position, amount]
/// startPos — стартовая позиция
/// k — максимум шагов
/// </summary>
public class Solution {
    public int MaxTotalFruits(int[][] fruits, int startPos, int k) {
        int n = fruits.Length;
        int left = 0, right = 0;
        int total = 0, res = 0;

        // Двигаем правый указатель по массиву
        for (; right < n; right++) {
            total += fruits[right][1];

            // Сдвигаем левый указатель, если текущий интервал нельзя пройти за k шагов
            while (left <= right && !IsReachable(fruits[left][0], fruits[right][0], startPos, k)) {
                total -= fruits[left][1];
                left++;
            }

            res = Math.Max(res, total);
        }

        return res;
    }

    // Проверка, можно ли дойти от startPos и охватить интервал [left, right] за k шагов
    private bool IsReachable(int left, int right, int startPos, int k) {
        int dist1 = Math.Abs(startPos - left) + (right - left);
        int dist2 = Math.Abs(startPos - right) + (right - left);
        return Math.Min(dist1, dist2) <= k;
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