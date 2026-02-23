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

class Solution {
public:
    int score(vector<string>& cards, char x) {
        int xid = x - 'a';
        vector<int> cntA(10, 0), cntB(10, 0);
        int cntC = 0;

        // Подсчёт карт, содержащих x
        for (const string& card : cards) {
            int c1 = card[0] - 'a';
            int c2 = card[1] - 'a';
            if (c1 == xid && c2 == xid) {
                ++cntC;
            } else if (c1 == xid) {
                ++cntA[c2];
            } else if (c2 == xid) {
                ++cntB[c1];
            }
            // иначе карта не содержит x — игнорируем
        }

        // Функция, возвращающая массив g[k] = k + max внутренних пар после удаления k карт
        auto computeG = [&](vector<int>& cnt) -> vector<int> {
            vector<int> vals;
            for (int i = 0; i < 10; ++i) {
                if (i != xid && cnt[i] > 0) {
                    vals.push_back(cnt[i]);
                }
            }
            sort(vals.rbegin(), vals.rend()); // убывание
            vals.push_back(0);                // фиктивная группа с 0
            int m = vals.size();
            vector<int> t(m, 0);               // пороговые значения
            for (int i = 1; i < m; ++i) {
                t[i] = t[i-1] + (vals[i-1] - vals[i]) * i;
            }
            int total = t[m-1];                 // общее количество карт в этом множестве
            vector<int> g(total + 1);
            for (int k = 0; k <= total; ++k) {
                // находим интервал, в котором лежит k
                int i = 0;
                while (i < m-1 && k >= t[i+1]) ++i;
                int maxRem;
                if (i < m-1) {
                    int groupCnt = i + 1;
                    maxRem = vals[i] - (k - t[i]) / groupCnt;
                } else {
                    maxRem = 0; // последний интервал (все карты удалены)
                }
                int rem = total - k;
                int pairs = min(rem / 2, rem - maxRem);
                g[k] = k + pairs;
            }
            return g;
        };

        vector<int> gA = computeG(cntA);
        vector<int> gB = computeG(cntB);
        int totalA = (int)gA.size() - 1;
        int totalB = (int)gB.size() - 1;

        int ans = 0;
        for (int cA = 0; cA <= min(cntC, totalA); ++cA) {
            int cB = min(cntC - cA, totalB);
            ans = max(ans, gA[cA] + gB[cB]);
        }
        return ans;
    }
};