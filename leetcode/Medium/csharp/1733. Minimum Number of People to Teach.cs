/**
 * https://leetcode.com/problems/minimum-number-of-people-to-teach/description/?envType=daily-question&envId=2025-09-10
 */

public class Solution {
    /// <summary>
    /// Найти минимальное число людей, которым нужно преподать один язык,
    /// чтобы все дружеские пары могли общаться (имели хотя бы один общий язык).
    /// Алгоритм:
    /// 1. Определяем проблемные пары друзей, которые не имеют общего языка.
    /// 2. Собираем множество пользователей из этих пар.
    /// 3. Для каждого языка считаем, сколько из этих пользователей его знают.
    /// 4. Выбираем язык, который знают максимально много пользователей.
    /// 5. Ответ = число проблемных пользователей - максимум.
    /// </summary>
    public int MinimumTeachings(int n, int[][] languages, int[][] friendships) {
        var bad = new HashSet<int>();
        
        foreach (var f in friendships) {
            int u = f[0] - 1;
            int v = f[1] - 1;

            var setU = new HashSet<int>(languages[u]);
            bool ok = false;
            foreach (int lang in languages[v]) {
                if (setU.Contains(lang)) {
                    ok = true;
                    break;
                }
            }

            if (!ok) {
                bad.Add(u);
                bad.Add(v);
            }
        }

        if (bad.Count == 0) return 0;

        int[] cnt = new int[n + 1];
        foreach (int u in bad) {
            foreach (int lang in languages[u]) {
                cnt[lang]++;
            }
        }

        int maxKnown = 0;
        foreach (int c in cnt) {
            if (c > maxKnown) maxKnown = c;
        }

        return bad.Count - maxKnown;
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