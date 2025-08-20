/**
 * https://leetcode.com/problems/fruits-into-baskets-iii/description/?envType=daily-question&envId=2025-08-06
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Сегментное дерево по максимуму:
     * - query_first_ge(x): самый левый индекс i с baskets[i] >= x, иначе -1.
     * - update(i, -1): пометить корзину занятой.
     *
     * Сложность: O(n log n) времени, O(n) памяти.
     */
    int numOfUnplacedFruits(vector<int>& fruits, vector<int>& baskets) {
        int n = (int)baskets.size();
        if (n == 0) return 0;

        int size = 1;
        while (size < n) size <<= 1;
        vector<long long> seg(size << 1, -1);

        // build
        for (int i = 0; i < n; ++i) seg[size + i] = baskets[i];
        for (int i = size - 1; i > 0; --i) seg[i] = max(seg[i << 1], seg[i << 1 | 1]);

        auto query_first_ge = [&](long long x) -> int {
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
        };

        auto update = [&](int pos, long long val) {
            int i = pos + size;
            seg[i] = val;
            for (i >>= 1; i > 0; i >>= 1) {
                seg[i] = max(seg[i << 1], seg[i << 1 | 1]);
            }
        };

        int unplaced = 0;
        for (int f : fruits) {
            int i = query_first_ge(f);
            if (i == -1) ++unplaced;
            else update(i, -1);
        }
        return unplaced;
    }
};

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