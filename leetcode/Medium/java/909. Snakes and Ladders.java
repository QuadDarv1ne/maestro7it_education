/**
 * https://leetcode.com/problems/snakes-and-ladders/description/?envType=study-plan-v2&envId=top-interview-150
 */

import java.util.*;

class Solution {
    public int snakesAndLadders(int[][] board) {
        int n = board.length;
        int[] board1D = new int[n * n];

        int idx = 0;
        boolean leftToRight = true;
        for (int r = n - 1; r >= 0; r--) {
            if (leftToRight) {
                for (int c = 0; c < n; c++) {
                    board1D[idx++] = board[r][c];
                }
            } else {
                for (int c = n - 1; c >= 0; c--) {
                    board1D[idx++] = board[r][c];
                }
            }
            leftToRight = !leftToRight;
        }

        boolean[] visited = new boolean[n * n];
        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{0, 0});
        visited[0] = true;

        while (!queue.isEmpty()) {
            int[] curr = queue.poll();
            int pos = curr[0];
            int steps = curr[1];

            if (pos == n * n - 1) {
                return steps;
            }

            for (int i = 1; i <= 6; i++) {
                int nextPos = pos + i;
                if (nextPos < n * n) {
                    if (board1D[nextPos] != -1) {
                        nextPos = board1D[nextPos] - 1;
                    }
                    if (!visited[nextPos]) {
                        visited[nextPos] = true;
                        queue.offer(new int[]{nextPos, steps + 1});
                    }
                }
            }
        }

        return -1;
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