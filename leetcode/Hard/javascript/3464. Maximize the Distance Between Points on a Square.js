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

var maxDistance = function(side, points, k) {
    const n = points.length;
    const pos = new Array(n);
    for (let i = 0; i < n; ++i) {
        const [x, y] = points[i];
        if (y === 0) pos[i] = x;
        else if (x === side) pos[i] = side + y;
        else if (y === side) pos[i] = 2 * side + (side - x);
        else pos[i] = 3 * side + (side - y);
    }
    pos.sort((a, b) => a - b);

    const perimeter = 4 * side;
    const extended = new Array(2 * n);
    for (let i = 0; i < n; ++i) {
        extended[i] = pos[i];
        extended[i + n] = pos[i] + perimeter;
    }

    let low = 0, high = 2 * side, ans = 0;
    while (low <= high) {
        const mid = Math.floor((low + high) / 2);
        if (canPlace(extended, n, k, mid, perimeter)) {
            ans = mid;
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return ans;

    function canPlace(extended, n, k, d, perimeter) {
        for (let start = 0; start < n; ++start) {
            let cnt = 1;
            let lastPos = extended[start];
            let curIdx = start;
            while (cnt < k) {
                const target = lastPos + d;
                let nextIdx = binarySearch(extended, target, curIdx + 1, start + n);
                if (nextIdx === -1) break;
                curIdx = nextIdx;
                lastPos = extended[curIdx];
                ++cnt;
            }
            if (cnt === k && extended[start] + perimeter - lastPos >= d)
                return true;
        }
        return false;
    }

    function binarySearch(arr, target, left, right) {
        let lo = left, hi = right - 1;
        while (lo <= hi) {
            const mid = Math.floor((lo + hi) / 2);
            if (arr[mid] < target) lo = mid + 1;
            else if (arr[mid] > target) hi = mid - 1;
            else return mid;
        }
        return lo < right ? lo : -1;
    }
};