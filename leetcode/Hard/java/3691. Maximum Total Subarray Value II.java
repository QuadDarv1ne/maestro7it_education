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

class SparseTableRMQ {
    int n, maxLog;
    int[][] fMax, fMin;
    int[] lg;

    SparseTableRMQ(int[] data) {
        n = data.length;
        maxLog = 32 - Integer.numberOfLeadingZeros(n) + 1;
        fMax = new int[n][maxLog];
        fMin = new int[n][maxLog];
        lg = new int[n + 1];

        for (int i = 2; i <= n; i++)
            lg[i] = lg[i >> 1] + 1;

        for (int i = 0; i < n; i++) {
            fMax[i][0] = data[i];
            fMin[i][0] = data[i];
        }

        for (int j = 1; j < maxLog; j++) {
            int step = 1 << (j - 1);
            for (int i = 0; i <= n - (1 << j); i++) {
                fMax[i][j] = Math.max(fMax[i][j - 1], fMax[i + step][j - 1]);
                fMin[i][j] = Math.min(fMin[i][j - 1], fMin[i + step][j - 1]);
            }
        }
    }

    int queryMax(int l, int r) {
        int k = lg[r - l + 1];
        return Math.max(fMax[l][k], fMax[r - (1 << k) + 1][k]);
    }

    int queryMin(int l, int r) {
        int k = lg[r - l + 1];
        return Math.min(fMin[l][k], fMin[r - (1 << k) + 1][k]);
    }
}

class Solution {
    public long maxTotalValue(int[] nums, int k) {
        int n = nums.length;
        SparseTableRMQ st = new SparseTableRMQ(nums);
        
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(b[0], a[0]));

        for (int l = 0; l < n; l++) {
            long val = st.queryMax(l, n - 1) - st.queryMin(l, n - 1);
            pq.offer(new long[]{val, l, n - 1});
        }

        long ans = 0;
        for (int i = 0; i < k; i++) {
            long[] curr = pq.poll();
            long val = curr[0];
            int l = (int) curr[1];
            int r = (int) curr[2];
            ans += val;
            if (r > l) {
                long nextVal = st.queryMax(l, r - 1) - st.queryMin(l, r - 1);
                pq.offer(new long[]{nextVal, l, r - 1});
            }
        }
        return ans;
    }
}