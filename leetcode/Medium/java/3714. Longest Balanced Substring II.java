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

import java.util.*;

class Solution {
    public int longestBalanced(String s) {
        int n = s.length();
        int ans = 0;

        // Случай 1: один символ
        for (char ch : new char[]{'a', 'b', 'c'}) {
            int cur = 0;
            for (char c : s.toCharArray()) {
                if (c == ch) cur++;
                else cur = 0;
                ans = Math.max(ans, cur);
            }
        }

        // Случай 2: два символа
        char[][] pairs = {{'a','b'}, {'a','c'}, {'b','c'}};
        for (char[] p : pairs) {
            char x = p[0], y = p[1];
            char third = (char)('a' + 'b' + 'c' - x - y);
            String[] segments = s.split(String.valueOf(third));
            for (String seg : segments) {
                int m = seg.length();
                if (m < 2) continue;
                int[] prefX = new int[m + 1];
                int[] prefY = new int[m + 1];
                for (int i = 0; i < m; i++) {
                    prefX[i + 1] = prefX[i] + (seg.charAt(i) == x ? 1 : 0);
                    prefY[i + 1] = prefY[i] + (seg.charAt(i) == y ? 1 : 0);
                }
                Map<Integer, Integer> firstOcc = new HashMap<>();
                int diff = 0;
                firstOcc.put(0, 0);
                for (int i = 1; i <= m; i++) {
                    if (seg.charAt(i - 1) == x) diff++;
                    else if (seg.charAt(i - 1) == y) diff--;
                    if (firstOcc.containsKey(diff)) {
                        int start = firstOcc.get(diff);
                        if (prefX[i] - prefX[start] > 0 && prefY[i] - prefY[start] > 0) {
                            ans = Math.max(ans, i - start);
                        }
                    } else {
                        firstOcc.put(diff, i);
                    }
                }
            }
        }

        // Случай 3: три символа
        Map<Pair, Node> occ = new HashMap<>();
        occ.put(new Pair(0, 0), new Node(-1, 0, 0, 0));
        int cntA = 0, cntB = 0, cntC = 0;
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (c == 'a') cntA++;
            else if (c == 'b') cntB++;
            else cntC++;
            Pair key = new Pair(cntB - cntA, cntC - cntA);
            if (occ.containsKey(key)) {
                Node node = occ.get(key);
                if (cntA - node.ca > 0 && cntB - node.cb > 0 && cntC - node.cc > 0) {
                    ans = Math.max(ans, i - node.idx);
                }
            } else {
                occ.put(key, new Node(i, cntA, cntB, cntC));
            }
        }

        return ans;
    }

    class Pair {
        int a, b;
        Pair(int a, int b) { this.a = a; this.b = b; }
        public boolean equals(Object o) {
            if (!(o instanceof Pair)) return false;
            Pair p = (Pair) o;
            return a == p.a && b == p.b;
        }
        public int hashCode() { return 31 * a + b; }
    }

    class Node {
        int idx, ca, cb, cc;
        Node(int i, int a, int b, int c) { idx = i; ca = a; cb = b; cc = c; }
    }
}