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

using System;
using System.Collections.Generic;

/**
 * Разреженная таблица (Sparse Table) для O(1) запросов
 * минимума и максимума на отрезке.
 * 
 * Предподсчёт: O(n log n)
 * Запрос: O(1)
 * Память: O(n log n)
 * 
 * Автор: Дуплей Максим Игоревич
 */
public class SparseTableRMQ {
    int n, maxLog;
    int[,] fMax, fMin;
    int[] lg;

    public SparseTableRMQ(int[] data) {
        n = data.Length;
        maxLog = (int)Math.Log2(n) + 2;
        fMax = new int[n, maxLog];
        fMin = new int[n, maxLog];
        lg = new int[n + 1];

        for (int i = 2; i <= n; i++)
            lg[i] = lg[i >> 1] + 1;

        for (int i = 0; i < n; i++) {
            fMax[i, 0] = data[i];
            fMin[i, 0] = data[i];
        }

        for (int j = 1; j < maxLog; j++) {
            int step = 1 << (j - 1);
            for (int i = 0; i <= n - (1 << j); i++) {
                fMax[i, j] = Math.Max(fMax[i, j - 1], fMax[i + step, j - 1]);
                fMin[i, j] = Math.Min(fMin[i, j - 1], fMin[i + step, j - 1]);
            }
        }
    }

    public int QueryMax(int l, int r) {
        int k = lg[r - l + 1];
        return Math.Max(fMax[l, k], fMax[r - (1 << k) + 1, k]);
    }

    public int QueryMin(int l, int r) {
        int k = lg[r - l + 1];
        return Math.Min(fMin[l, k], fMin[r - (1 << k) + 1, k]);
    }
}

public class Solution {
    /**
     * Находит максимальную суммарную ценность k подмассивов.
     * 
     * Ценность подмассива = max - min. Для каждого левого края l
     * ценность монотонно возрастает с ростом правого края r.
     * 
     * Алгоритм:
     * 1. Строим ST-таблицу для O(1) запросов min/max
     * 2. Для каждого l помещаем в max-кучу подмассив [l, n-1]
     * 3. k раз извлекаем максимум и добавляем в кучу [l, r-1]
     * 
     * @param nums Массив целых чисел
     * @param k Количество выбираемых подмассивов
     * @return Максимальная суммарная ценность k подмассивов
     * 
     * Сложность:
     * Время: O(n log n + k log n)
     * Память: O(n log n)
     * 
     * Автор: Дуплей Максим Игоревич
     */
    public long MaxTotalValue(int[] nums, int k) {
        int n = nums.Length;
        var st = new SparseTableRMQ(nums);
        
        // Max-куча: используем отрицательный приоритет
        var pq = new PriorityQueue<(long val, int l, int r), long>();

        for (int l = 0; l < n; l++) {
            long val = st.QueryMax(l, n - 1) - st.QueryMin(l, n - 1);
            pq.Enqueue((val, l, n - 1), -val);
        }

        long ans = 0;
        for (int i = 0; i < k; i++) {
            var (val, l, r) = pq.Dequeue();
            ans += val;
            if (r > l) {
                long nextVal = st.QueryMax(l, r - 1) - st.QueryMin(l, r - 1);
                pq.Enqueue((nextVal, l, r - 1), -nextVal);
            }
        }
        return ans;
    }
}