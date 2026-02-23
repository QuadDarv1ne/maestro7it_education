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
using System.Collections.Generic;

public class Solution {
    public int Score(string[] cards, char x) {
        int xid = x - 'a';
        int[] cntA = new int[10];
        int[] cntB = new int[10];
        int cntC = 0;

        foreach (string card in cards) {
            int a = card[0] - 'a';
            int b = card[1] - 'a';
            if (a == xid && b == xid) {
                cntC++;
            } else if (a == xid) {
                cntA[b]++;
            } else if (b == xid) {
                cntB[a]++;
            }
        }

        int[] gA = ComputeG(cntA);
        int[] gB = ComputeG(cntB);
        int totalA = gA.Length - 1;
        int totalB = gB.Length - 1;

        int ans = 0;
        for (int cA = 0; cA <= Math.Min(cntC, totalA); cA++) {
            int cB = Math.Min(cntC - cA, totalB);
            ans = Math.Max(ans, gA[cA] + gB[cB]);
        }
        return ans;
    }

    private int[] ComputeG(int[] cnt) {
        List<int> list = new List<int>();
        foreach (int c in cnt) if (c > 0) list.Add(c);
        list.Sort((a, b) => b.CompareTo(a));
        list.Add(0);
        int m = list.Count;
        int[] vals = list.ToArray();

        int[] t = new int[m];
        for (int i = 1; i < m; i++) {
            t[i] = t[i-1] + (vals[i-1] - vals[i]) * i;
        }

        int total = 0;
        foreach (int c in cnt) total += c;
        int[] g = new int[total + 1];

        for (int k = 0; k <= total; k++) {
            int i = 0;
            while (i < m - 1 && k >= t[i+1]) i++;
            int groupCnt = i + 1;
            int maxRem = vals[i] - (k - t[i]) / groupCnt;
            int rem = total - k;
            int pairs = Math.Min(rem / 2, rem - maxRem);
            g[k] = k + pairs;
        }
        return g;
    }
}
