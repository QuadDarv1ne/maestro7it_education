/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
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
 * Решение задачи "XOR After Range Multiplication Queries II".
 * 
 * @description Метод: декомпозиция на квадратный корень (sqrt decomposition)
 * 
 * @algorithm
 * 1. Порог B = √n разделяет запросы на "малые" (k ≤ B) и "большие" (k > B)
 * 2. Большие k: прямое применение умножения по индексам
 * 3. Малые k: группировка по (k, l%k) + разностный массив с мультипликативными обновлениями
 * 4. Применение через префиксное произведение и модульную инверсию
 * 
 * @complexity
 * - Время: O(q·√n + n·√n)
 * - Память: O(n + q)
 * 
 * @param {number[]} nums - исходный массив целых чисел
 * @param {number[][]} queries - список запросов [l, r, k, v]
 * @return {number} - побитовый XOR всех элементов после обработки
 * 
 * @author Дуплей М.И.
 * @source {@link https://github.com/QuadDarv1ne/}
 */
var xorAfterQueries = function(nums, queries) {
    const MOD = 1_000_000_007n;
    const n = nums.length;
    if (n === 0) return 0;
    
    const B = Math.floor(Math.sqrt(n)) + 1;
    const arr = nums.map(x => BigInt(x));
    const smallQueries = new Map();
    
    const modPow = (base, exp, mod) => {
        let result = 1n;
        base %= mod;
        while (exp > 0n) {
            if (exp & 1n) result = (result * base) % mod;
            base = (base * base) % mod;
            exp >>= 1n;
        }
        return result;
    };
    
    const modInv = (a) => modPow(a, MOD - 2n, MOD);
    
    for (const [l, r, k, v] of queries) {
        if (k > B) {
            for (let idx = l; idx <= r; idx += k) {
                arr[idx] = (arr[idx] * BigInt(v)) % MOD;
            }
        } else {
            const mod = l % k;
            const posL = Math.floor((l - mod) / k);
            const posR = Math.floor((r - mod) / k);
            const key = `${k},${mod}`;
            if (!smallQueries.has(key)) smallQueries.set(key, []);
            smallQueries.get(key).push([posL, posR, v]);
        }
    }
    
    for (const [key, qList] of smallQueries) {
        const [kStr, modStr] = key.split(',');
        const k = parseInt(kStr);
        const mod = parseInt(modStr);
        const size = Math.ceil((n - mod) / k);
        const diff = new Array(size + 2).fill(1n);
        
        for (const [posL, posR, v] of qList) {
            const bv = BigInt(v);
            diff[posL] = (diff[posL] * bv) % MOD;
            diff[posR + 1] = (diff[posR + 1] * modInv(bv)) % MOD;
        }
        
        let mult = 1n;
        for (let pos = 0; pos < size; pos++) {
            mult = (mult * diff[pos]) % MOD;
            const idx = mod + pos * k;
            if (idx < n) arr[idx] = (arr[idx] * mult) % MOD;
        }
    }
    
    let result = 0;
    for (const val of arr) result ^= Number(val);
    return result;
};