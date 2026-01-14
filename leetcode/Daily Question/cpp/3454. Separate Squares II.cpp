/**
 * Разделение квадратов II - решение на C++
 * Алгоритм сканирующей прямой с деревом отрезков
 * 
 * @param squares: vector<vector<int>> - квадраты [x, y, длина]
 * @return: double - минимальная y-координата линии, делящей площадь пополам
 * 
 * Сложность: O(n log n) время, O(n) память.
 * 
 * Алгоритм:
 * 1. Сбор уникальных X-координат и создание дерева отрезков
 * 2. Создание и сортировка событий (начало/конец квадратов)
 * 3. Первый проход: вычисление общей площади
 * 4. Второй проход: поиск y, где накопленная площадь = половине общей
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

#include <vector>
#include <set>
#include <algorithm>
#include <tuple>

using namespace std;

// Класс дерева отрезков для отслеживания покрытой ширины на оси X
class SegmentTree {
private:
    int n;                      // Количество отрезков (xs.size() - 1)
    vector<long long> xs;       // Отсортированные уникальные X-координаты
    vector<int> cnt;            // Счетчик покрытий для каждого узла
    vector<long long> width;    // Покрытая ширина для каждого узла
    
    // Рекурсивное обновление дерева
    void update(int idx, int l, int r, long long ql, long long qr, int val) {
        // Если текущий отрезок не пересекается с запросом
        if (qr <= xs[l] || xs[r + 1] <= ql) return;
        
        // Если текущий отрезок полностью покрыт запросом
        if (ql <= xs[l] && xs[r + 1] <= qr) {
            cnt[idx] += val;
        } else {
            // Иначе рекурсивно обновляем детей
            int mid = (l + r) / 2;
            update(idx * 2 + 1, l, mid, ql, qr, val);
            update(idx * 2 + 2, mid + 1, r, ql, qr, val);
        }
        
        // Пересчитываем покрытую ширину для текущего узла
        if (cnt[idx] > 0) {
            width[idx] = xs[r + 1] - xs[l];
        } else if (l == r) {
            width[idx] = 0;
        } else {
            width[idx] = width[idx * 2 + 1] + width[idx * 2 + 2];
        }
    }

public:
    // Конструктор
    SegmentTree(const vector<long long>& xs_list) {
        xs = xs_list;
        n = xs.size() - 1;
        cnt.assign(4 * n, 0);
        width.assign(4 * n, 0);
    }
    
    // Добавление значения к интервалу [l, r)
    void add(long long l, long long r, int val) {
        if (l < r) {
            update(0, 0, n - 1, l, r, val);
        }
    }
    
    // Получение общей покрытой ширины
    long long getCoveredWidth() const {
        return width[0];
    }
};

class Solution {
public:
    double separateSquares(vector<vector<int>>& squares) {
        // 1. Создаем события и собираем уникальные X-координаты
        vector<tuple<long long, int, long long, long long>> events;
        set<long long> xs_set;
        
        for (const auto& sq : squares) {
            long long x = sq[0];
            long long y = sq[1];
            long long l = sq[2];
            long long xr = x + l;
            
            // Событие начала квадрата (+1)
            events.emplace_back(y, 1, x, xr);
            // Событие конца квадрата (-1)
            events.emplace_back(y + l, -1, x, xr);
            
            xs_set.insert(x);
            xs_set.insert(xr);
        }
        
        // 2. Сортируем события по y
        sort(events.begin(), events.end(), 
             [](const auto& a, const auto& b) { return get<0>(a) < get<0>(b); });
        
        // 3. Преобразуем set в vector для дерева отрезков
        vector<long long> xs(xs_set.begin(), xs_set.end());
        
        // 4. Вычисляем общую площадь
        double totalArea = calculateTotalArea(events, xs);
        double halfArea = totalArea / 2.0;
        
        // 5. Поиск разделяющей линии (второй проход)
        SegmentTree tree(xs);
        double accumulated = 0.0;
        long long prevY = 0;
        
        for (const auto& event : events) {
            long long y = get<0>(event);
            int delta = get<1>(event);
            long long xl = get<2>(event);
            long long xr = get<3>(event);
            
            long long covered = tree.getCoveredWidth();
            
            // Если есть покрытие, проверяем не достигли ли halfArea
            if (covered > 0) {
                double areaGain = covered * (y - prevY);
                if (accumulated + areaGain >= halfArea - 1e-12) {
                    // Нашли точку, где накопленная площадь равна halfArea
                    return prevY + (halfArea - accumulated) / covered;
                }
                accumulated += areaGain;
            }
            
            // Обновляем дерево отрезков
            tree.add(xl, xr, delta);
            prevY = y;
        }
        
        // Если не нашли (все квадраты ниже линии), возвращаем последний y
        return prevY;
    }
    
private:
    // Вспомогательная функция для вычисления общей площади
    double calculateTotalArea(const vector<tuple<long long, int, long long, long long>>& events,
                             const vector<long long>& xs) {
        SegmentTree tree(xs);
        double total = 0.0;
        long long prevY = 0;
        
        for (const auto& event : events) {
            long long y = get<0>(event);
            int delta = get<1>(event);
            long long xl = get<2>(event);
            long long xr = get<3>(event);
            
            total += tree.getCoveredWidth() * (y - prevY);
            tree.add(xl, xr, delta);
            prevY = y;
        }
        
        return total;
    }
};