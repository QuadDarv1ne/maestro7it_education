/**
 * https://leetcode.com/problems/maximum-walls-destroyed-by-robots/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Maximum Walls Destroyed by Robots" на JavaScript
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
 * 5. Используем бинарный поиск (lowerBound) для подсчёта стен в интервале
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

/**
 * @param {number[]} robots
 * @param {number[]} distance
 * @param {number[]} walls
 * @return {number}
 */
var maxWalls = function(robots, distance, walls) {
    const n = robots.length;
    const arr = robots.map((r, i) => [r, distance[i]]);
    arr.sort((a, b) => a[0] - b[0]);
    walls.sort((a, b) => a - b);
    
    const f = Array.from({ length: n }, () => Array(2).fill(-1));
    
    function lowerBound(arr, target) {
        let left = 0, right = arr.length;
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return left;
    }
    
    function dfs(i, j) {
        if (i < 0) {
            return 0;
        }
        if (f[i][j] !== -1) {
            return f[i][j];
        }
        
        let left = arr[i][0] - arr[i][1];
        if (i > 0) {
            left = Math.max(left, arr[i - 1][0] + 1);
        }
        let l = lowerBound(walls, left);
        let r = lowerBound(walls, arr[i][0] + 1);
        let ans = dfs(i - 1, 0) + (r - l);
        
        let right = arr[i][0] + arr[i][1];
        if (i + 1 < n) {
            if (j === 0) {
                right = Math.min(right, arr[i + 1][0] - arr[i + 1][1] - 1);
            } else {
                right = Math.min(right, arr[i + 1][0] - 1);
            }
        }
        l = lowerBound(walls, arr[i][0]);
        r = lowerBound(walls, right + 1);
        ans = Math.max(ans, dfs(i - 1, 1) + (r - l));
        
        f[i][j] = ans;
        return ans;
    }
    
    return dfs(n - 1, 1);
};