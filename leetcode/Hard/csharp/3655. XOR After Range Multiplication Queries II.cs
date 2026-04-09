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

/// <summary>
/// Решение задачи "XOR After Range Multiplication Queries II".
/// </summary>
/// <remarks>
/// <para><b>Метод:</b> декомпозиция на квадратный корень (sqrt decomposition)</para>
/// <para><b>Алгоритм:</b></para>
/// <list type="bullet">
///   <item>Порог B = √n для разделения запросов по значению k</item>
///   <item>k > B: прямое применение умножения (итерация по индексам)</item>
///   <item>k ≤ B: группировка по (k, l%k) + разностный массив</item>
///   <item>Мультипликативные обновления через модульную инверсию</item>
/// </list>
/// <para><b>Сложность:</b></para>
/// <list type="bullet">
///   <item>Время: O(q·√n + n·√n)</item>
///   <item>Память: O(n + q)</item>
/// </list>
/// </remarks>
/// <param name="nums">Исходный массив целых чисел</param>
/// <param name="queries">Список запросов [l, r, k, v]</param>
/// <returns>Побитовый XOR всех элементов после обработки</returns>
/// <author>Дуплей М.И.</author>
/// <source>https://github.com/QuadDarv1ne/</source>

using System;
using System.Collections.Generic;

public class Solution {
    private const long MOD = 1_000_000_007L;
    
    // Быстрое возведение в степень по модулю
    private long ModPow(long baseVal, long exp, long mod) {
        long result = 1;
        baseVal %= mod;
        while (exp > 0) {
            if ((exp & 1) == 1) result = (result * baseVal) % mod;
            baseVal = (baseVal * baseVal) % mod;
            exp >>= 1;
        }
        return result;
    }
    
    // Модульная инверсия (малая теорема Ферма)
    private long ModInv(long a) => ModPow(a, MOD - 2, MOD);
    
    // Ключ для хеширования пары (k, mod)
    private long MakeKey(int k, int mod) => ((long)k << 20) | mod;
    
    public int XorAfterQueries(int[] nums, int[][] queries) {
        int n = nums.Length;
        if (n == 0) return 0;
        
        int B = (int)Math.Sqrt(n) + 1;
        long[] arr = new long[n];
        for (int i = 0; i < n; i++) arr[i] = nums[i];
        
        // Группировка: key -> список (posL, posR, v)
        var smallQueries = new Dictionary<long, List<(int, int, int)>>();
        
        foreach (var q in queries) {
            int l = q[0], r = q[1], k = q[2], v = q[3];
            
            if (k > B) {
                // Прямое применение для больших k
                for (int idx = l; idx <= r; idx += k) {
                    arr[idx] = (arr[idx] * v) % MOD;
                }
            } else {
                int mod = l % k;
                int posL = (l - mod) / k;
                int posR = (r - mod) / k;
                long key = MakeKey(k, mod);
                
                if (!smallQueries.ContainsKey(key)) {
                    smallQueries[key] = new List<(int, int, int)>();
                }
                smallQueries[key].Add((posL, posR, v));
            }
        }
        
        // Обработка малых запросов
        foreach (var entry in smallQueries) {
            long key = entry.Key;
            int k = (int)(key >> 20);
            int mod = (int)(key & ((1 << 20) - 1));
            
            int size = (n - mod + k - 1) / k;
            long[] diff = new long[size + 2];
            Array.Fill(diff, 1L);
            
            foreach (var (posL, posR, v) in entry.Value) {
                diff[posL] = (diff[posL] * v) % MOD;
                diff[posR + 1] = (diff[posR + 1] * ModInv(v)) % MOD;
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
        foreach (long val in arr) {
            result ^= (int)val;
        }
        return result;
    }
}