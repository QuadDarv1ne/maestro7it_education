/**
 * https://leetcode.com/problems/implement-router/description/?envType=daily-question&envId=2025-09-20
 *
 * Класс Router — модель маршрутизатора с ограниченной памятью.
 */

using System;
using System.Collections.Generic;

/*
 * Реализация Router с явными lower/upper bound — корректно считает дубликаты.
 */
public class Router {
    private int memoryLimit;
    private Queue<(int,int,int)> q;
    private HashSet<string> seen;
    private Dictionary<int, List<int>> destMap;
    private Dictionary<int, int> startIndex;

    public Router(int memoryLimit) {
        this.memoryLimit = memoryLimit;
        this.q = new Queue<(int,int,int)>();
        this.seen = new HashSet<string>();
        this.destMap = new Dictionary<int, List<int>>();
        this.startIndex = new Dictionary<int, int>();
    }

    private string MakeKey(int s, int d, int t) => $"{s}#{d}#{t}";

    public bool AddPacket(int source, int destination, int timestamp) {
        var key = MakeKey(source, destination, timestamp);
        if (seen.Contains(key)) return false;
        if (q.Count == memoryLimit) ForwardPacket();

        q.Enqueue((source, destination, timestamp));
        seen.Add(key);

        if (!destMap.ContainsKey(destination)) {
            destMap[destination] = new List<int>();
            startIndex[destination] = 0;
        }
        destMap[destination].Add(timestamp);
        return true;
    }

    public IList<int> ForwardPacket() {
        if (q.Count == 0) return new List<int>();
        var (s, d, t) = q.Dequeue();
        seen.Remove(MakeKey(s, d, t));

        if (destMap.TryGetValue(d, out var arr)) {
            int idx = startIndex.GetValueOrDefault(d, 0);
            while (idx < arr.Count && arr[idx] != t) idx++;
            if (idx < arr.Count && arr[idx] == t) idx++;
            startIndex[d] = idx;

            if (idx > 1000 && idx > arr.Count / 2) {
                var newArr = arr.GetRange(idx, arr.Count - idx);
                destMap[d] = newArr;
                startIndex[d] = 0;
            }
        }

        return new List<int>{s,d,t};
    }

    public int GetCount(int destination, int startTime, int endTime) {
        if (!destMap.TryGetValue(destination, out var arr)) return 0;
        int s = startIndex.GetValueOrDefault(destination, 0);
        if (s >= arr.Count) return 0;
        int L = LowerBound(arr, startTime, s, arr.Count);
        int R = UpperBound(arr, endTime, s, arr.Count);
        return R - L;
    }

    private int LowerBound(List<int> arr, int val, int l, int r) {
        int L = l, R = r;
        while (L < R) {
            int m = L + (R - L) / 2;
            if (arr[m] < val) L = m + 1;
            else R = m;
        }
        return L;
    }
    private int UpperBound(List<int> arr, int val, int l, int r) {
        int L = l, R = r;
        while (L < R) {
            int m = L + (R - L) / 2;
            if (arr[m] <= val) L = m + 1;
            else R = m;
        }
        return L;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/