import java.util.*;

/**
 * Решение для Separate Squares II на Java
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
class SegmentTree {
    int n;
    long[] xs;
    int[] cnt;
    long[] width;

    public SegmentTree(List<Long> xsList) {
        xs = new long[xsList.size()];
        for (int i = 0; i < xsList.size(); i++) xs[i] = xsList.get(i);
        n = xs.length - 1;
        cnt = new int[4 * n];
        width = new long[4 * n];
    }

    private void update(int idx, int l, int r, long ql, long qr, int val) {
        if (qr <= xs[l] || xs[r + 1] <= ql) return;
        if (ql <= xs[l] && xs[r + 1] <= qr) {
            cnt[idx] += val;
        } else {
            int mid = (l + r) / 2;
            update(idx * 2 + 1, l, mid, ql, qr, val);
            update(idx * 2 + 2, mid + 1, r, ql, qr, val);
        }
        
        if (cnt[idx] > 0) {
            width[idx] = xs[r + 1] - xs[l];
        } else if (l == r) {
            width[idx] = 0;
        } else {
            width[idx] = width[idx * 2 + 1] + width[idx * 2 + 2];
        }
    }

    public void add(long l, long r, int val) {
        if (l < r) update(0, 0, n - 1, l, r, val);
    }

    public long getCoveredWidth() {
        return width[0];
    }
}

class Solution {
    public double separateSquares(int[][] squares) {
        // Создаем события (y, delta, xl, xr) и собираем уникальные X
        List<long[]> events = new ArrayList<>();
        Set<Long> xsSet = new TreeSet<>();
        
        for (int[] sq : squares) {
            long x = sq[0], y = sq[1], l = sq[2];
            long xr = x + l;
            events.add(new long[]{y, 1, x, xr});
            events.add(new long[]{y + l, -1, x, xr});
            xsSet.add(x);
            xsSet.add(xr);
        }
        
        // Сортируем события по y
        events.sort(Comparator.comparingLong(a -> a[0]));
        
        // Подготовка массива X
        List<Long> xsList = new ArrayList<>(xsSet);
        
        // Вычисляем общую площадь
        double totalArea = calculateTotalArea(events, xsList);
        double halfArea = totalArea / 2.0;
        
        // Поиск разделяющей линии
        SegmentTree tree = new SegmentTree(xsList);
        double accumulated = 0.0;
        long prevY = 0;
        
        for (long[] event : events) {
            long y = event[0];
            int delta = (int)event[1];
            long xl = event[2], xr = event[3];
            
            long covered = tree.getCoveredWidth();
            if (covered > 0) {
                double areaGain = covered * (y - prevY);
                if (accumulated + areaGain >= halfArea - 1e-12) {
                    return prevY + (halfArea - accumulated) / covered;
                }
                accumulated += areaGain;
            }
            
            tree.add(xl, xr, delta);
            prevY = y;
        }
        
        return prevY;
    }
    
    private double calculateTotalArea(List<long[]> events, List<Long> xsList) {
        SegmentTree tree = new SegmentTree(xsList);
        double total = 0.0;
        long prevY = 0;
        
        for (long[] event : events) {
            long y = event[0];
            int delta = (int)event[1];
            long xl = event[2], xr = event[3];
            
            total += tree.getCoveredWidth() * (y - prevY);
            tree.add(xl, xr, delta);
            prevY = y;
        }
        
        return total;
    }
}