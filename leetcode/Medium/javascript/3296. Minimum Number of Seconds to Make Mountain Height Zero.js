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

/**
 * @param {number} mountainHeight
 * @param {number[]} workerTimes
 * @return {number}
 */
var minNumberOfSeconds = function(mountainHeight, workerTimes) {
    // Для точности используем BigInt, так как числа могут превышать 2^53
    const can = (T) => {
        let total = 0n;
        const target = BigInt(mountainHeight);
        for (const w of workerTimes) {
            const wBig = BigInt(w);
            // d = 1 + 8 * floor(T / w)
            const d = 1n + 8n * (T / wBig);
            const sqrt_d = sqrtBigInt(d);
            // Корректировка корня
            let s = sqrt_d;
            while ((s + 1n) * (s + 1n) <= d) s++;
            while (s * s > d) s--;
            const x = (s - 1n) / 2n;
            total += x;
            if (total >= target) return true;
        }
        return total >= target;
    };

    // Целочисленный квадратный корень для BigInt
    const sqrtBigInt = (value) => {
        if (value < 0n) throw new Error('negative');
        if (value < 2n) return value;
        let x = value;
        let y = (x + 1n) >> 1n;
        while (y < x) {
            x = y;
            y = (x + value / x) >> 1n;
        }
        return x;
    };

    let left = 0n;
    let right = 10n ** 18n; // 1e18
    while (left < right) {
        const mid = (left + right) >> 1n;
        if (can(mid)) {
            right = mid;
        } else {
            left = mid + 1n;
        }
    }
    return Number(left); // ответ гарантированно помещается в Number
};