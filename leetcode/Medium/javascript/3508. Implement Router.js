/**
 * https://leetcode.com/problems/implement-router/description/?envType=daily-question&envId=2025-09-20
 */

class Router {
    constructor(memoryLimit) {
        this.memoryLimit = memoryLimit;
        this.q = [];   // очередь пакетов
        this.seen = new Set();
        this.destMap = new Map();
        this.startIndex = new Map();
    }

    _makeKey(s,d,t) {
        return `${s}#${d}#${t}`;
    }

    addPacket(source, destination, timestamp) {
        let key = this._makeKey(source,destination,timestamp);
        if (this.seen.has(key)) return false;
        if (this.q.length === this.memoryLimit) this.forwardPacket();
        this.q.push([source,destination,timestamp]);
        this.seen.add(key);
        if (!this.destMap.has(destination)) {
            this.destMap.set(destination, []);
            this.startIndex.set(destination, 0);
        }
        this.destMap.get(destination).push(timestamp);
        return true;
    }

    forwardPacket() {
        if (this.q.length === 0) return [];
        let [s,d,t] = this.q.shift();
        this.seen.delete(this._makeKey(s,d,t));
        let arr = this.destMap.get(d);
        let idx = this.startIndex.get(d);
        if (arr[idx] === t) this.startIndex.set(d, idx+1);
        return [s,d,t];
    }

    getCount(destination, startTime, endTime) {
        if (!this.destMap.has(destination)) return 0;
        let arr = this.destMap.get(destination);
        let start = this.startIndex.get(destination);

        // бинарный поиск
        function lowerBound(a, x, from) {
            let l = from, r = a.length;
            while (l < r) {
                let m = Math.floor((l+r)/2);
                if (a[m] < x) l = m+1;
                else r = m;
            }
            return l;
        }
        function upperBound(a, x, from) {
            let l = from, r = a.length;
            while (l < r) {
                let m = Math.floor((l+r)/2);
                if (a[m] <= x) l = m+1;
                else r = m;
            }
            return l;
        }

        let L = lowerBound(arr, startTime, start);
        let R = upperBound(arr, endTime, start);
        return R - L;
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