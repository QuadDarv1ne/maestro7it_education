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

public class Solution {
    public int LongestBalanced(string s) {
        int n = s.Length;
        int ans = 0;

        // Случай 1: один символ
        foreach (char ch in new char[] {'a','b','c'}) {
            int cur = 0;
            foreach (char c in s) {
                if (c == ch) cur++;
                else cur = 0;
                ans = Math.Max(ans, cur);
            }
        }

        // Случай 2: два символа
        var pairs = new (char, char)[] {('a','b'), ('a','c'), ('b','c')};
        foreach (var (x, y) in pairs) {
            char third = (char)('a' + 'b' + 'c' - x - y);
            var segments = s.Split(third);
            foreach (var seg in segments) {
                int m = seg.Length;
                if (m < 2) continue;
                int[] prefX = new int[m + 1];
                int[] prefY = new int[m + 1];
                for (int i = 0; i < m; i++) {
                    prefX[i + 1] = prefX[i] + (seg[i] == x ? 1 : 0);
                    prefY[i + 1] = prefY[i] + (seg[i] == y ? 1 : 0);
                }
                var firstOcc = new Dictionary<int, int>();
                int diff = 0;
                firstOcc[0] = 0;
                for (int i = 1; i <= m; i++) {
                    if (seg[i - 1] == x) diff++;
                    else if (seg[i - 1] == y) diff--;
                    if (firstOcc.ContainsKey(diff)) {
                        int start = firstOcc[diff];
                        if (prefX[i] - prefX[start] > 0 && prefY[i] - prefY[start] > 0) {
                            ans = Math.Max(ans, i - start);
                        }
                    } else {
                        firstOcc[diff] = i;
                    }
                }
            }
        }

        // Случай 3: три символа
        var occ = new Dictionary<(int, int), (int idx, int ca, int cb, int cc)>();
        occ[(0, 0)] = (-1, 0, 0, 0);
        int cntA = 0, cntB = 0, cntC = 0;
        for (int i = 0; i < n; i++) {
            if (s[i] == 'a') cntA++;
            else if (s[i] == 'b') cntB++;
            else cntC++;
            var key = (cntB - cntA, cntC - cntA);
            if (occ.TryGetValue(key, out var val)) {
                if (cntA - val.ca > 0 && cntB - val.cb > 0 && cntC - val.cc > 0) {
                    ans = Math.Max(ans, i - val.idx);
                }
            } else {
                occ[key] = (i, cntA, cntB, cntC);
            }
        }

        return ans;
    }
}