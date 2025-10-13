/**
 * https://leetcode.com/problems/find-sum-of-array-product-of-magical-sequences/description/?envType=daily-question&envId=2025-10-12
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/ 
 */

const MOD = 1000000007n;

function magicalSum(m, k, nums) {
  const n = nums.length;
  if (m === 0) return k === 0 ? 1 : 0;
  if (k < 0) return 0;

  // Pascal C with BigInt
  const C = Array.from({ length: m + 1 }, () => Array(m + 1).fill(0n));
  for (let i = 0; i <= m; ++i) {
    C[i][0] = 1n;
    for (let j = 1; j <= i; ++j) {
      C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD;
    }
  }

  // pow_vals: BigInt
  const pow_vals = Array.from({ length: n }, () => Array(m + 1).fill(1n));
  for (let i = 0; i < n; ++i) {
    const base = BigInt(nums[i]) % MOD;
    for (let t = 1; t <= m; ++t) {
      pow_vals[i][t] = (pow_vals[i][t - 1] * base) % MOD;
    }
  }

  // dp[carry][used][pc] as BigInt
  let dp = Array.from({ length: m + 1 }, () =>
    Array.from({ length: m + 1 }, () => Array(k + 1).fill(0n))
  );
  dp[0][0][0] = 1n;

  for (let pos = 0; pos < n; ++pos) {
    let dp_next = Array.from({ length: m + 1 }, () =>
      Array.from({ length: m + 1 }, () => Array(k + 1).fill(0n))
    );
    for (let carry = 0; carry <= m; ++carry) {
      for (let used = 0; used <= m; ++used) {
        const rem = m - used;
        for (let pc = 0; pc <= k; ++pc) {
          const cur = dp[carry][used][pc];
          if (cur === 0n) continue;
          for (let take = 0; take <= rem; ++take) {
            const prod_mul = pow_vals[pos][take]; // BigInt
            const ways_mul = C[rem][take];        // BigInt
            let total_mul = (cur * prod_mul) % MOD;
            total_mul = (total_mul * ways_mul) % MOD;

            const total_at_pos = carry + take;
            const bit = total_at_pos & 1;
            const carry2 = total_at_pos >> 1;
            const pc2 = pc + bit;
            if (pc2 > k || carry2 > m) continue;
            const used2 = used + take;
            dp_next[carry2][used2][pc2] = (dp_next[carry2][used2][pc2] + total_mul) % MOD;
          }
        }
      }
    }
    dp = dp_next;
  }

  let ans = 0n;
  for (let carry = 0; carry <= m; ++carry) {
    const carry_bits = popcount(carry);
    for (let pc = 0; pc <= k; ++pc) {
      const val = dp[carry][m][pc];
      if (val === 0n) continue;
      const final_pc = pc + carry_bits;
      if (final_pc === k) ans = (ans + val) % MOD;
    }
  }
  return Number(ans); // вернуть как Number (в пределах MOD)
}

// вспомогательная функция popcount для небольших целых (m <= ~30)
function popcount(x) {
  let cnt = 0;
  while (x > 0) {
    cnt += x & 1;
    x >>= 1;
  }
  return cnt;
}

// Экспорт для окружений, где это нужно (runner/тесты)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { magicalSum };
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