/**
 * https://leetcode.com/problems/maximum-average-pass-ratio/description/?envType=daily-question&envId=2025-09-01
 */

// Java — LeetCode
import java.util.PriorityQueue;

class Solution {
    static class Node {
        int p, t;
        Node(int p, int t) { this.p = p; this.t = t; }
        double gain() { return (double)(p + 1) / (t + 1) - (double)p / t; }
    }

    public double maxAverageRatio(int[][] classes, int extraStudents) {
        PriorityQueue<Node> pq = new PriorityQueue<>((a, b) -> Double.compare(b.gain(), a.gain()));
        for (int[] c : classes) pq.offer(new Node(c[0], c[1]));
        while (extraStudents-- > 0) {
            Node cur = pq.poll();
            cur.p += 1; cur.t += 1;
            pq.offer(cur);
        }
        double sum = 0.0;
        while (!pq.isEmpty()) {
            Node n = pq.poll();
            sum += (double)n.p / n.t;
        }
        return sum / classes.length;
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