/**
 * https://leetcode.com/problems/maximum-walls-destroyed-by-robots/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Maximum Walls Destroyed by Robots" на C#
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
 * 5. Используем Array.BinarySearch для подсчёта стен в интервале
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

public class Solution {
    private int?[,] f;
    private int[][] arr;
    private int[] walls;
    private int n;

    public int MaxWalls(int[] robots, int[] distance, int[] walls) {
        n = robots.Length;
        arr = new int[n][];
        for (int i = 0; i < n; i++) {
            arr[i] = new int[] { robots[i], distance[i] };
        }
        Array.Sort(arr, (a, b) => a[0].CompareTo(b[0]));
        Array.Sort(walls);
        this.walls = walls;
        f = new int?[n, 2];
        return Dfs(n - 1, 1);
    }

    private int Dfs(int i, int j) {
        if (i < 0) {
            return 0;
        }
        if (f[i, j].HasValue) {
            return f[i, j].Value;
        }

        int left = arr[i][0] - arr[i][1];
        if (i > 0) {
            left = Math.Max(left, arr[i - 1][0] + 1);
        }
        int l = LowerBound(walls, left);
        int r = LowerBound(walls, arr[i][0] + 1);
        int ans = Dfs(i - 1, 0) + (r - l);

        int right = arr[i][0] + arr[i][1];
        if (i + 1 < n) {
            if (j == 0) {
                right = Math.Min(right, arr[i + 1][0] - arr[i + 1][1] - 1);
            } else {
                right = Math.Min(right, arr[i + 1][0] - 1);
            }
        }
        l = LowerBound(walls, arr[i][0]);
        r = LowerBound(walls, right + 1);
        ans = Math.Max(ans, Dfs(i - 1, 1) + (r - l));

        f[i, j] = ans;
        return ans;
    }

    private int LowerBound(int[] arr, int target) {
        int idx = Array.BinarySearch(arr, target);
        if (idx < 0) {
            return -idx - 1;
        }
        return idx;
    }
}