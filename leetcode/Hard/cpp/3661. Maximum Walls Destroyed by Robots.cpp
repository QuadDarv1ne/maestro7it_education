/**
 * https://leetcode.com/problems/maximum-walls-destroyed-by-robots/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Maximum Walls Destroyed by Robots" на C++
 * 
 * Задача: Даны роботы с позициями и дальностью стрельбы, а также стены.
 * Каждый робот может выстрелить один раз влево или вправо.
 * Пуля останавливается при встрече с другим роботом.
 * Нужно найти максимальное количество уникальных стен, которые можно разрушить.
 * 
 * Алгоритм:
 * 1. Сортируем роботов по позиции и объединяем с их дальностью
 * 2. Сортируем стены для бинарного поиска
 * 3. Используем динамическое программирование с мемоизацией (DFS):
 *    - f[i][0] - макс. стен для первых i+1 роботов, где i-й стрелял влево
 *    - f[i][1] - макс. стен для первых i+1 роботов, где i-й стрелял вправо
 * 4. Для каждого робота:
 *    - Выстрел влево: левая граница = max(позиция - дальность, позиция предыдущего + 1)
 *    - Выстрел вправо: правая граница зависит от направления следующего робота
 * 5. Используем бинарный поиск (ranges::lower_bound) для подсчёта стен в интервале
 * 
 * Сложность: O((n+m) log m) времени, O(n) памяти
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
    int maxWalls(vector<int>& robots, vector<int>& distance, vector<int>& walls) {
        int n = robots.size();
        vector<pair<int, int>> arr(n);
        for (int i = 0; i < n; i++) {
            arr[i] = {robots[i], distance[i]};
        }
        ranges::sort(arr, {}, &pair<int, int>::first);
        ranges::sort(walls);

        vector f(n, vector<int>(2, -1));

        auto dfs = [&](this auto&& dfs, int i, int j) -> int {
            if (i < 0) {
                return 0;
            }
            if (f[i][j] != -1) {
                return f[i][j];
            }

            int left = arr[i].first - arr[i].second;
            if (i > 0) {
                left = max(left, arr[i - 1].first + 1);
            }
            int l = ranges::lower_bound(walls, left) - walls.begin();
            int r = ranges::lower_bound(walls, arr[i].first + 1) - walls.begin();
            int ans = dfs(i - 1, 0) + (r - l);

            int right = arr[i].first + arr[i].second;
            if (i + 1 < n) {
                if (j == 0) {
                    right = min(right, arr[i + 1].first - arr[i + 1].second - 1);
                } else {
                    right = min(right, arr[i + 1].first - 1);
                }
            }
            l = ranges::lower_bound(walls, arr[i].first) - walls.begin();
            r = ranges::lower_bound(walls, right + 1) - walls.begin();
            ans = max(ans, dfs(i - 1, 1) + (r - l));

            return f[i][j] = ans;
        };

        return dfs(n - 1, 1);
    }
};