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
    public int score(String[] cards, char x) {
        int xid = x - 'a';
        int[] cntA = new int[10];
        int[] cntB = new int[10];
        int cntC = 0;

        for (String card : cards) {
            int a = card.charAt(0) - 'a';
            int b = card.charAt(1) - 'a';
            if (a == xid && b == xid) {
                cntC++;
            } else if (a == xid) {
                cntA[b]++;
            } else if (b == xid) {
                cntB[a]++;
            }
        }

        int[] gA = computeG(cntA);
        int[] gB = computeG(cntB);
        int totalA = gA.length - 1;
        int totalB = gB.length - 1;

        int ans = 0;
        for (int cA = 0; cA <= Math.min(cntC, totalA); cA++) {
            int cB = Math.min(cntC - cA, totalB);
            ans = Math.max(ans, gA[cA] + gB[cB]);
        }
        return ans;
    }

    private int[] computeG(int[] cnt) {
        List<Integer> list = new ArrayList<>();
        for (int c : cnt) if (c > 0) list.add(c);
        Collections.sort(list, Collections.reverseOrder());
        list.add(0);
        int m = list.size();
        int[] vals = new int[m];
        for (int i = 0; i < m; i++) vals[i] = list.get(i);

        int[] t = new int[m];
        for (int i = 1; i < m; i++) {
            t[i] = t[i-1] + (vals[i-1] - vals[i]) * i;
        }

        int total = 0;
        for (int c : cnt) total += c;
        int[] g = new int[total + 1];

        for (int k = 0; k <= total; k++) {
            int i = 0;
            while (i < m - 1 && k >= t[i+1]) i++;
            int groupCnt = i + 1;
            int maxRem = vals[i] - (k - t[i]) / groupCnt;
            int rem = total - k;
            int pairs = Math.min(rem / 2, rem - maxRem);
            g[k] = k + pairs;
        }
        return g;
    }
}
