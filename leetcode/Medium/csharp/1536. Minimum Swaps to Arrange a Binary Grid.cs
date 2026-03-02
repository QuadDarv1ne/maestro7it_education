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

public class Solution {
    public int MinSwaps(int[][] grid) {
        int n = grid.Length;
        // Вычисляем количество нулей в конце каждой строки
        int[] trailing = new int[n];
        for (int i = 0; i < n; i++) {
            int cnt = 0;
            for (int j = n - 1; j >= 0; j--) {
                if (grid[i][j] == 0) {
                    cnt++;
                } else {
                    break;
                }
            }
            trailing[i] = cnt;
        }
        
        int ans = 0;
        for (int i = 0; i < n; i++) {
            int required = n - 1 - i;
            // ищем строку с требуемым количеством нулей, начиная с i
            int j = i;
            while (j < n && trailing[j] < required) {
                j++;
            }
            if (j == n) {
                return -1;
            }
            // добавляем свопы
            ans += j - i;
            // сдвигаем элементы с i по j-1 вправо, а элемент j ставим на i
            int val = trailing[j];
            for (int k = j; k > i; k--) {
                trailing[k] = trailing[k - 1];
            }
            trailing[i] = val;
        }
        return ans;
    }
}