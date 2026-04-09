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
import java.util.*;

class Solution {
    private static final long MOD = 1_000_000_007L;
    
    // Быстрое возведение в степень по модулю
    private long modPow(long base, long exp, long mod) {
        long result = 1;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1) == 1) result = (result * base) % mod;
            base = (base * base) % mod;
            exp >>= 1;
        }
        return result;
    }
    
    // Модульная инверсия (теорема Ферма)
    private long modInv(long a) {
        return modPow(a, MOD - 2, MOD);
    }
    
    // Ключ для хеширования пары (k, mod)
    private long makeKey(int k, int mod) {
        return ((long) k << 20) | mod;
    }
    
    public int xorAfterQueries(int[] nums, int[][] queries) {
        int n = nums.length;
        if (n == 0) return 0;
        
        int B = (int) Math.sqrt(n) + 1;
        long[] arr = new long[n];
        for (int i = 0; i < n; i++) arr[i] = nums[i];
        
        // Группировка малых запросов: key -> список (posL, posR, v)
        Map<Long, List<int[]>> smallQueries = new HashMap<>();
        
        for (int[] q : queries) {
            int l = q[0], r = q[1], k = q[2], v = q[3];
            
            if (k > B) {
                // Большие k: прямое применение
                for (int idx = l; idx <= r; idx += k) {
                    arr[idx] = (arr[idx] * v) % MOD;
                }
            } else {
                int mod = l % k;
                int posL = (l - mod) / k;
                int posR = (r - mod) / k;
                long key = makeKey(k, mod);
                
                smallQueries.computeIfAbsent(key, x -> new ArrayList<>())
                           .add(new int[]{posL, posR, v});
            }
        }
        
        // Обработка малых запросов через разностный массив
        for (Map.Entry<Long, List<int[]>> entry : smallQueries.entrySet()) {
            long key = entry.getKey();
            int k = (int) (key >> 20);
            int mod = (int) (key & ((1 << 20) - 1));
            
            int size = (n - mod + k - 1) / k;
            long[] diff = new long[size + 2];
            Arrays.fill(diff, 1L);
            
            for (int[] q : entry.getValue()) {
                int posL = q[0], posR = q[1], v = q[2];
                diff[posL] = (diff[posL] * v) % MOD;
                diff[posR + 1] = (diff[posR + 1] * modInv(v)) % MOD;
            }
            
            long mult = 1;
            for (int pos = 0; pos < size; pos++) {
                mult = (mult * diff[pos]) % MOD;
                int idx = mod + pos * k;
                if (idx < n) {
                    arr[idx] = (arr[idx] * mult) % MOD;
                }
            }
        }
        
        // Финальный XOR
        int result = 0;
        for (long val : arr) {
            result ^= (int) val;
        }
        return result;
    }
}