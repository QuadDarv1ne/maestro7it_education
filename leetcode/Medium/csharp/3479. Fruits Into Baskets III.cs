/**
 * https://leetcode.com/problems/fruits-into-baskets-iii/description/?envType=daily-question&envId=2025-08-06
 */

public class Solution {
    /// <summary>
    /// Подсчитывает количество неразмещённых фруктов.
    /// Используется сегментное дерево по максимуму:
    /// - Запрос: найти самый левый индекс i с baskets[i] >= fruit.
    /// - Обновление: пометить корзину занятой (значение = -1).
    /// Сложность: O(n log n) времени, O(n) памяти.
    /// </summary>
    public int NumOfUnplacedFruits(int[] fruits, int[] baskets) {
        int n = baskets.Length;
        if (n == 0) return 0;

        int size = 1;
        while (size < n) size <<= 1;
        int[] seg = new int[size << 1];
        for (int i = 0; i < seg.Length; i++) seg[i] = -1;

        // build
        for (int i = 0; i < n; i++) seg[size + i] = baskets[i];
        for (int i = size - 1; i > 0; --i) seg[i] = System.Math.Max(seg[i << 1], seg[i << 1 | 1]);

        int QueryFirstGE(int x) {
            int idx = 1;
            if (seg[idx] < x) return -1;
            int l = 0, r = size - 1;
            while (l != r) {
                int left = idx << 1;
                int mid = (l + r) >> 1;
                if (seg[left] >= x) {
                    idx = left;
                    r = mid;
                } else {
                    idx = left | 1;
                    l = mid + 1;
                }
            }
            return (l < n) ? l : -1;
        }

        void Update(int pos, int val) {
            int i = pos + size;
            seg[i] = val;
            for (i >>= 1; i > 0; i >>= 1) {
                seg[i] = System.Math.Max(seg[i << 1], seg[i << 1 | 1]);
            }
        }

        int unplaced = 0;
        foreach (var f in fruits) {
            int i = QueryFirstGE(f);
            if (i == -1) unplaced++;
            else Update(i, -1);
        }
        return unplaced;
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