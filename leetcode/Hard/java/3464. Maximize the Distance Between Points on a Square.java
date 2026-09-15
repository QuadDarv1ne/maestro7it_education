import java.util.*;

class Solution {
    public int maxDistance(int side, int[][] points, int k) {
        int n = points.length;
        long[] pos = new long[n];
        for (int i = 0; i < n; ++i) {
            int x = points[i][0], y = points[i][1];
            if (y == 0) pos[i] = x;
            else if (x == side) pos[i] = (long)side + y;
            else if (y == side) pos[i] = 2L * side + (side - x);
            else pos[i] = 3L * side + (side - y);
        }
        Arrays.sort(pos);

        long perimeter = 4L * side;
        long[] extended = new long[2 * n];
        for (int i = 0; i < n; ++i) {
            extended[i] = pos[i];
            extended[i + n] = pos[i] + perimeter;
        }

        long low = 0, high = 2L * side, ans = 0;
        while (low <= high) {
            long mid = (low + high) / 2;
            if (canPlace(extended, n, k, mid, perimeter)) {
                ans = mid;
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return (int)ans;
    }

    private boolean canPlace(long[] extended, int n, int k, long d, long perimeter) {
        for (int start = 0; start < n; ++start) {
            int cnt = 1;
            long lastPos = extended[start];
            int curIdx = start;
            while (cnt < k) {
                long target = lastPos + d;
                int from = curIdx + 1;
                int to = start + n; // exclusive
                if (from >= to) break;
                int nextIdx = Arrays.binarySearch(extended, from, to, target);
                if (nextIdx < 0) nextIdx = -nextIdx - 1;
                if (nextIdx >= to) break;
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