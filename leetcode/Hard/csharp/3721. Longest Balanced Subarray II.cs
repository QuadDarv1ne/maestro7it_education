/**
 * https://leetcode.com/problems/longest-balanced-subarray-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "3721. Longest Balanced Subarray II"
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

/*
 * https://leetcode.com/problems/longest-balanced-subarray-ii/description/
 * Решение задачи "3721. Longest Balanced Subarray II"
 *
 * Используется дерево отрезков с ленивым обновлением.
 * Для каждого числа: +1 (нечётное), -1 (чётное).
 * Поддерживается префиксная сумма "now" и словарь last[] с последней позицией числа.
 * Дерево отрезков хранит для каждой левой границы текущий баланс [l, i].
 * Операции: range_add, query – поиск наименьшего индекса с заданным балансом.
 * Сложность: O(n log n).
 */

using System;
using System.Collections.Generic;

public class Solution
{
    // Узел дерева отрезков
    private class Node
    {
        public int l, r;     // границы отрезка индексов левых границ
        public int mn, mx;   // минимум и максимум баланса на отрезке
        public int lazy;     // отложенное добавление
    }

    // Дерево отрезков с ленивым обновлением
    private class SegmentTree
    {
        private Node[] tr;
        private int n;

        public SegmentTree(int n)
        {
            this.n = n;
            tr = new Node[(n + 1) * 4];
            for (int i = 0; i < tr.Length; i++)
                tr[i] = new Node();
            Build(1, 0, n);
        }

        // Построение пустого дерева (все балансы = 0)
        private void Build(int u, int l, int r)
        {
            tr[u].l = l;
            tr[u].r = r;
            tr[u].mn = tr[u].mx = 0;
            tr[u].lazy = 0;
            if (l == r) return;
            int mid = (l + r) >> 1;
            Build(u << 1, l, mid);
            Build(u << 1 | 1, mid + 1, r);
        }

        // Применение добавки к узлу
        private void Apply(int u, int v)
        {
            tr[u].mn += v;
            tr[u].mx += v;
            tr[u].lazy += v;
        }

        // Проталкивание ленивой метки
        private void PushDown(int u)
        {
            if (tr[u].lazy != 0)
            {
                Apply(u << 1, tr[u].lazy);
                Apply(u << 1 | 1, tr[u].lazy);
                tr[u].lazy = 0;
            }
        }

        // Обновление узла от детей
        private void PushUp(int u)
        {
            tr[u].mn = Math.Min(tr[u << 1].mn, tr[u << 1 | 1].mn);
            tr[u].mx = Math.Max(tr[u << 1].mx, tr[u << 1 | 1].mx);
        }

        // Добавить v ко всем балансам на отрезке [l, r]
        public void Modify(int u, int l, int r, int v)
        {
            if (tr[u].l >= l && tr[u].r <= r)
            {
                Apply(u, v);
                return;
            }
            PushDown(u);
            int mid = (tr[u].l + tr[u].r) >> 1;
            if (l <= mid) Modify(u << 1, l, r, v);
            if (r > mid) Modify(u << 1 | 1, l, r, v);
            PushUp(u);
        }

        // Найти наименьший индекс pos такой, что баланс[pos] == target
        public int Query(int u, int target)
        {
            if (tr[u].l == tr[u].r) return tr[u].l;
            PushDown(u);
            int lc = u << 1, rc = u << 1 | 1;
            if (tr[lc].mn <= target && target <= tr[lc].mx)
                return Query(lc, target);
            return Query(rc, target);
        }
    }

    public int LongestBalanced(int[] nums)
    {
        int n = nums.Length;
        SegmentTree st = new SegmentTree(n);
        Dictionary<int, int> last = new Dictionary<int, int>();

        int now = 0;   // текущая префиксная сумма
        int ans = 0;

        for (int i = 1; i <= n; i++)
        {
            int x = nums[i - 1];
            int det = (x & 1) == 1 ? 1 : -1;

            if (last.ContainsKey(x))
            {
                // убираем вклад предыдущего вхождения
                st.Modify(1, last[x], n, -det);
                now -= det;
            }

            last[x] = i;
            st.Modify(1, i, n, det);
            now += det;

            int pos = st.Query(1, now); // самый ранний индекс с таким балансом
            ans = Math.Max(ans, i - pos);
        }

        return ans;
    }
}