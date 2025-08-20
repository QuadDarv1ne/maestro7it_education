/**
 * https://leetcode.com/problems/fruits-into-baskets-iii/description/?envType=daily-question&envId=2025-08-06
 */

class Solution {
    /**
     * Сегментное дерево по максимуму для поиска самого левого индекса i,
     * где baskets[i] >= fruit, и последующего «занятия» корзины.
     *
     * Время: O(n log n), память: O(n).
     */
    int size;
    int[] seg;
    int n;

    public int numOfUnplacedFruits(int[] fruits, int[] baskets) {
        n = baskets.length;
        if (n == 0) return 0;

        size = 1;
        while (size < n) size <<= 1;
        seg = new int[size << 1];
        for (int i = 0; i < seg.length; i++) seg[i] = -1;

        // build
        for (int i = 0; i < n; i++) seg[size + i] = baskets[i];
        for (int i = size - 1; i > 0; --i) seg[i] = Math.max(seg[i << 1], seg[i << 1 | 1]);

        int unplaced = 0;
        for (int f : fruits) {
            int i = queryFirstGE(f);
            if (i == -1) unplaced++;
            else update(i, -1);
        }
        return unplaced;
    }

    // Поиск самого левого индекса i, где baskets[i] >= x
    private int queryFirstGE(int x) {
        int idx = 1;
        if (seg[idx] < x) return -1;
        int l = 0, r = size - 1;
        while (l != r) {
            int left = idx << 1;
            int mid = (l + r) >>> 1;
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

    // Помечаем корзину занятой (baskets[pos] = val)
    private void update(int pos, int val) {
        int i = pos + size;
        seg[i] = val;
        for (i >>= 1; i > 0; i >>= 1) {
            seg[i] = Math.max(seg[i << 1], seg[i << 1 | 1]);
        }
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