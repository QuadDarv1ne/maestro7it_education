/**
 * https://leetcode.com/problems/find-sum-of-array-product-of-magical-sequences/description/?envType=daily-question&envId=2025-10-12
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/ 
 */

using System;
using System.Numerics; // для BitOperations.PopCount (в .NET Core / .NET 5+)
public class Solution {
    const long MOD = 1000000007L;
    public int magicalSum(int m, int k, int[] nums) {
        int n = nums.Length;
        if (m == 0) return (k == 0) ? 1 : 0;
        if (k < 0) return 0;

        long[,] tmp;
        // Pascal C
        long[][] C = new long[m+1][];
        for (int i = 0; i <= m; ++i) {
            C[i] = new long[m+1];
            C[i][0] = 1;
            for (int j = 1; j <= i; ++j)
                C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD;
        }

        // pow_vals
        long[][] pow_vals = new long[n][];
        for (int i = 0; i < n; ++i) {
            pow_vals[i] = new long[m+1];
            pow_vals[i][0] = 1;
            long baseVal = nums[i] % MOD;
            for (int t = 1; t <= m; ++t)
                pow_vals[i][t] = (pow_vals[i][t-1] * baseVal) % MOD;
        }

        // dp[carry][used][pc]
        long[][][] dp = new long[m+1][][];
        for (int i = 0; i <= m; ++i) {
            dp[i] = new long[m+1][];
            for (int j = 0; j <= m; ++j)
                dp[i][j] = new long[k+1];
        }
        dp[0][0][0] = 1;

        for (int pos = 0; pos < n; ++pos) {
            long[][][] dp_next = new long[m+1][][];
            for (int i = 0; i <= m; ++i) {
                dp_next[i] = new long[m+1][];
                for (int j = 0; j <= m; ++j) dp_next[i][j] = new long[k+1];
            }

            for (int carry = 0; carry <= m; ++carry) {
                for (int used = 0; used <= m; ++used) {
                    if (used > m) continue;
                    int rem = m - used;
                    for (int pc = 0; pc <= k; ++pc) {
                        long cur = dp[carry][used][pc];
                        if (cur == 0) continue;
                        for (int take = 0; take <= rem; ++take) {
                            long prod_mul = pow_vals[pos][take];
                            long ways_mul = C[rem][take];
                            long total_mul = cur * prod_mul % MOD;
                            total_mul = total_mul * ways_mul % MOD;

                            int total_at_pos = carry + take;
                            int bit = total_at_pos & 1;
                            int carry2 = total_at_pos >> 1;
                            int pc2 = pc + bit;
                            if (pc2 > k || carry2 > m) continue;
                            int used2 = used + take;
                            dp_next[carry2][used2][pc2] = (dp_next[carry2][used2][pc2] + total_mul) % MOD;
                        }
                    }
                }
            }
            dp = dp_next;
        }

        long ans = 0;
        for (int carry = 0; carry <= m; ++carry) {
            int carry_bits = System.Numerics.BitOperations.PopCount((uint)carry);
            for (int pc = 0; pc <= k; ++pc) {
                long val = dp[carry][m][pc];
                if (val == 0) continue;
                int final_pc = pc + carry_bits;
                if (final_pc == k) ans = (ans + val) % MOD;
            }
        }
        return (int)ans;
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
# 8. Официальный сайт школы Maestro7IT: https://school-maestro7it.ru/
*/