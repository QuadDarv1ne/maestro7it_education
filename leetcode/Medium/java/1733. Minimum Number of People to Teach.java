/**
 * https://leetcode.com/problems/minimum-number-of-people-to-teach/description/?envType=daily-question&envId=2025-09-10
 */

class Solution {
    /**
     * Найти минимальное число людей, которым нужно преподать один язык,
     * чтобы все дружеские пары могли общаться (имели хотя бы один общий язык).
     * Алгоритм:
     * 1. Находим все проблемные пары друзей, у которых нет общих языков.
     * 2. Собираем множество пользователей из этих пар.
     * 3. Для каждого языка считаем, сколько из этих пользователей его знают.
     * 4. Выбираем язык, который знают максимально много из них.
     * 5. Ответ = число проблемных пользователей - максимум.
     */
    public int minimumTeachings(int n, int[][] languages, int[][] friendships) {
        Set<Integer> bad = new HashSet<>();

        for (int[] f : friendships) {
            int u = f[0] - 1;
            int v = f[1] - 1;

            boolean ok = false;
            // проверяем есть ли общий язык
            for (int lu : languages[u]) {
                for (int lv : languages[v]) {
                    if (lu == lv) {
                        ok = true;
                        break;
                    }
                }
                if (ok) break;
            }

            if (!ok) {
                bad.add(u);
                bad.add(v);
            }
        }

        if (bad.isEmpty()) return 0;

        int[] cnt = new int[n + 1];
        for (int u : bad) {
            for (int lang : languages[u]) {
                cnt[lang]++;
            }
        }

        int maxKnown = 0;
        for (int c : cnt) {
            if (c > maxKnown) maxKnown = c;
        }

        return bad.size() - maxKnown;
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