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
    public int[] getBiggestThree(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        // Используем TreeSet для хранения уникальных отсортированных значений
        TreeSet<Integer> sums = new TreeSet<>();

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                // Ромб размера 1
                sums.add(grid[i][j]);
                if (sums.size() > 3) sums.pollFirst();

                int maxK = Math.min(Math.min(i, m - 1 - i), Math.min(j, n - 1 - j)) + 1;
                for (int k = 2; k <= maxK; k++) {
                    int total = 0;
                    int r1 = i - (k - 1), c1 = j;
                    int r2 = i, c2 = j + (k - 1);
                    int r3 = i + (k - 1), c3 = j;
                    int r4 = i, c4 = j - (k - 1);

                    // Верх -> Право
                    for (int s = 0; s < k - 1; s++) total += grid[r1 + s][c1 + s];
                    // Право -> Низ
                    for (int s = 0; s < k - 1; s++) total += grid[r2 + s][c2 - s];
                    // Низ -> Лево
                    for (int s = 0; s < k - 1; s++) total += grid[r3 - s][c3 - s];
                    // Лево -> Верх
                    for (int s = 0; s < k - 1; s++) total += grid[r4 - s][c4 + s];

                    sums.add(total);
                    if (sums.size() > 3) sums.pollFirst();
                }
            }
        }

        // Преобразуем TreeSet в массив в порядке убывания
        int[] result = new int[sums.size()];
        int index = sums.size() - 1;
        for (int val : sums) {
            result[index--] = val;
        }
        return result;
    }
}