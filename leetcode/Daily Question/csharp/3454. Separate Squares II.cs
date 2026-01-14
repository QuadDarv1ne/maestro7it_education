using System;
using System.Collections.Generic;

/**
 * Решение для Separate Squares II на C#
 * Использует алгоритм сканирующей прямой с деревом отрезков
 * 
 * Сложность: O(n log n) время, O(n) память.
 * Алгоритм:
 * 1. Сбор уникальных X-координат и создание дерева отрезков
 * 2. Создание и сортировка событий (начало/конец квадратов)
 * 3. Первый проход: вычисление общей площади
 * 4. Второй проход: поиск y, где накопленная площадь = половина
 * 
 * Автор: Дуплей Максим Игоревич
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
public class SegmentTree {
    private int n;
    private long[] xs;
    private int[] cnt;
    private long[] width;
    
    public SegmentTree(List<long> xsList) {
        xs = xsList.ToArray();
        n = xs.Length - 1;
        cnt = new int[4 * n];
        width = new long[4 * n];
    }
    
    private void Update(int idx, int l, int r, long ql, long qr, int val) {
        if (qr <= xs[l] || xs[r + 1] <= ql) return;
        
        if (ql <= xs[l] && xs[r + 1] <= qr) {
            cnt[idx] += val;
        } else {
            int mid = (l + r) / 2;
            Update(idx * 2 + 1, l, mid, ql, qr, val);
            Update(idx * 2 + 2, mid + 1, r, ql, qr, val);
        }
        
        if (cnt[idx] > 0) {
            width[idx] = xs[r + 1] - xs[l];
        } else if (l == r) {
            width[idx] = 0;
        } else {
            width[idx] = width[idx * 2 + 1] + width[idx * 2 + 2];
        }
    }
    
    public void Add(long l, long r, int val) {
        if (l < r) Update(0, 0, n - 1, l, r, val);
    }
    
    public long GetCoveredWidth() {
        return width[0];
    }
}

public class Solution {
    public double SeparateSquares(int[][] squares) {
        // Создаем события и собираем уникальные X
        List<(long y, int delta, long xl, long xr)> events = new();
        SortedSet<long> xsSet = new();
        
        foreach (var sq in squares) {
            long x = sq[0], y = sq[1], l = sq[2];
            long xr = x + l;
            events.Add((y, 1, x, xr));
            events.Add((y + l, -1, x, xr));
            xsSet.Add(x);
            xsSet.Add(xr);
        }
        
        // Сортируем события по y
        events.Sort((a, b) => a.y.CompareTo(b.y));
        
        // Подготовка массива X
        List<long> xsList = new(xsSet);
        
        // Вычисляем общую площадь
        double totalArea = CalculateTotalArea(events, xsList);
        double halfArea = totalArea / 2.0;
        
        // Поиск разделяющей линии
        SegmentTree tree = new(xsList);
        double accumulated = 0.0;
        long prevY = 0;
        
        foreach (var ev in events) {
            long covered = tree.GetCoveredWidth();
            if (covered > 0) {
                double areaGain = covered * (ev.y - prevY);
                if (accumulated + areaGain >= halfArea - 1e-12) {
                    return prevY + (halfArea - accumulated) / covered;
                }
                accumulated += areaGain;
            }
            
            tree.Add(ev.xl, ev.xr, ev.delta);
            prevY = ev.y;
        }
        
        return prevY;
    }
    
    private double CalculateTotalArea(List<(long y, int delta, long xl, long xr)> events, 
                                      List<long> xsList) {
        SegmentTree tree = new(xsList);
        double total = 0.0;
        long prevY = 0;
        
        foreach (var ev in events) {
            total += tree.GetCoveredWidth() * (ev.y - prevY);
            tree.Add(ev.xl, ev.xr, ev.delta);
            prevY = ev.y;
        }
        
        return total;
    }
}