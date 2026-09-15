/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

using System;
using System.Linq;

public class Solution {
    public int MaxDistance(int side, int[][] points, int k) {
        int n = points.Length;
        long[] pos = new long[n];
        for (int i = 0; i < n; ++i) {
            int x = points[i][0], y = points[i][1];
            if (y == 0) pos[i] = x;
            else if (x == side) pos[i] = side + (long)y;
            else if (y == side) pos[i] = 2L * side + (side - x);
            else pos[i] = 3L * side + (side - y);
        }
        Array.Sort(pos);

        long perimeter = 4L * side;
        long[] extended = new long[2 * n];
        for (int i = 0; i < n; ++i) {
            extended[i] = pos[i];
            extended[i + n] = pos[i] + perimeter;
        }

        long low = 0, high = 2L * side, ans = 0;
        while (low <= high) {
            long mid = (low + high) / 2;
            if (CanPlace(extended, n, k, mid, perimeter)) {
                ans = mid;
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return (int)ans;
    }

    private bool CanPlace(long[] extended, int n, int k, long d, long perimeter) {
        for (int start = 0; start < n; ++start) {
            int cnt = 1;
            long lastPos = extended[start];
            int curIdx = start;
            while (cnt < k) {
                long target = lastPos + d;
                // Ищем позицию, начиная с curIdx+1, не выходя за start+n
                int left = curIdx + 1;
                int right = start + n - 1;
                if (left > right) break;
                int nextIdx = Array.BinarySearch(extended, left, right - left + 1, target);
                if (nextIdx < 0) nextIdx = ~nextIdx;
                if (nextIdx > right) break;
                curIdx = nextIdx;
                lastPos = extended[curIdx];
                ++cnt;
            }
            if (cnt == k && extended[start] + perimeter - lastPos >= d)
                return true;
        }
        return false;
    }
}