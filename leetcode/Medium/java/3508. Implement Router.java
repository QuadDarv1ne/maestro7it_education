/**
 * https://leetcode.com/problems/implement-router/description/?envType=daily-question&envId=2025-09-20
 *
 * Класс Router — модель маршрутизатора с ограниченной памятью.
 * 
 * Методы:
 *  - addPacket(s,d,t): добавляет пакет, возвращает false, если дубликат.
 *  - forwardPacket(): удаляет и возвращает старый пакет (FIFO).
 *  - getCount(d, start, end): возвращает число пакетов с заданным destination и временем в интервале.
 */

import java.util.*;

/**
 * Реализация Router с корректным подсчётом для дубликатов timestamp.
 */
class Router {
    private int memoryLimit;
    private Queue<int[]> q;
    private Set<String> seen;
    private Map<Integer, List<Integer>> destMap;
    private Map<Integer, Integer> startIndex;

    public Router(int memoryLimit) {
        this.memoryLimit = memoryLimit;
        this.q = new LinkedList<>();
        this.seen = new HashSet<>();
        this.destMap = new HashMap<>();
        this.startIndex = new HashMap<>();
    }

    private String makeKey(int s, int d, int t) {
        return s + "#" + d + "#" + t;
    }

    public boolean addPacket(int source, int destination, int timestamp) {
        String key = makeKey(source, destination, timestamp);
        if (seen.contains(key)) return false;
        if (q.size() == memoryLimit) forwardPacket();

        q.offer(new int[]{source, destination, timestamp});
        seen.add(key);

        destMap.putIfAbsent(destination, new ArrayList<>());
        startIndex.putIfAbsent(destination, 0);
        destMap.get(destination).add(timestamp);
        return true;
    }

    public int[] forwardPacket() {
        if (q.isEmpty()) return new int[]{};

        int[] p = q.poll();
        int s = p[0], d = p[1], t = p[2];
        seen.remove(makeKey(s, d, t));

        List<Integer> arr = destMap.get(d);
        if (arr != null) {
            int idx = startIndex.getOrDefault(d, 0);
            // продвигаем до первого matching timestamp
            while (idx < arr.size() && arr.get(idx) != t) idx++;
            if (idx < arr.size() && arr.get(idx) == t) idx++;
            startIndex.put(d, idx);

            // подрезка для экономии памяти
            if (idx > 1000 && idx > arr.size() / 2) {
                List<Integer> newArr = new ArrayList<>(arr.subList(idx, arr.size()));
                destMap.put(d, newArr);
                startIndex.put(d, 0);
            }
        }

        return p;
    }

    public int getCount(int destination, int startTime, int endTime) {
        List<Integer> arr = destMap.get(destination);
        if (arr == null) return 0;
        int s = startIndex.getOrDefault(destination, 0);
        if (s >= arr.size()) return 0;

        int L = lowerBound(arr, startTime, s, arr.size());
        int R = upperBound(arr, endTime, s, arr.size());
        return R - L;
    }

    // первый индекс i in [l, r) такой что arr[i] >= val
    private int lowerBound(List<Integer> arr, int val, int l, int r) {
        int L = l, R = r;
        while (L < R) {
            int m = L + (R - L) / 2;
            if (arr.get(m) < val) L = m + 1;
            else R = m;
        }
        return L;
    }

    // первый индекс i in [l, r) такой что arr[i] > val
    private int upperBound(List<Integer> arr, int val, int l, int r) {
        int L = l, R = r;
        while (L < R) {
            int m = L + (R - L) / 2;
            if (arr.get(m) <= val) L = m + 1;
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