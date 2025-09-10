/**
 * https://leetcode.com/problems/minimum-number-of-people-to-teach/description/?envType=daily-question&envId=2025-09-10
 */

class Solution {
public:
    /**
     * Найти минимальное число людей, которым нужно преподать один язык,
     * чтобы все друзья могли общаться (имели общий язык).
     * Подбор: язык, который знают наиболее часто среди проблемных пользователей — минимизируем обучение.
     */
    int minimumTeachings(int n, vector<vector<int>>& languages, vector<vector<int>>& friendships) {
        unordered_set<int> bad;
        for (auto &f : friendships) {
            int u = f[0] - 1, v = f[1] - 1;
            bool ok = false;
            for (int lu : languages[u]) 
                for (int lv : languages[v]) 
                    if (lu == lv) { ok = true; break; }
            if (!ok) {
                bad.insert(u);
                bad.insert(v);
            }
        }
        if (bad.empty()) return 0;
        vector<int> cnt(n + 1, 0);
        for (int u : bad)
            for (int lang : languages[u])
                cnt[lang]++;
        int maxKnown = *max_element(cnt.begin(), cnt.end());
        return bad.size() - maxKnown;
    }
};

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