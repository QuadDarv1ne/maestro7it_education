/**
 * https://leetcode.com/contest/weekly-contest-463/problems/xor-after-range-multiplication-queries-ii/
 */

import java.math.BigInteger;
class Solution {
    public int xorAfterQueries(int[] nums, int[][] queries) {
        long[] mul = new long[nums.length];
        for (int i = 0; i < nums.length; i++) {
            mul[i] = 1;
        }
        HashMap<Integer, HashMap<Integer, TreeMap<Integer, Long>>> diff = new HashMap<>();
        for (int[] query : queries) {
            if (query[2] > Math.sqrt(nums.length)) {
                for (int i = query[0]; i <= query[1]; i += query[2]) {
                    mul[i] = mul[i] * query[3] % 1000000007;
                }
            } else {
                diff.computeIfAbsent(query[2], t -> new HashMap<>()).computeIfAbsent(query[0] % query[2], t -> new TreeMap<>()).put(query[0] / query[2], diff.get(query[2]).get(query[0] % query[2]).getOrDefault(query[0] / query[2], 1L) * query[3] % 1000000007);
                diff.get(query[2]).get(query[0] % query[2]).put((query[1] - query[0] % query[2]) / query[2] + 1, diff.get(query[2]).get(query[0] % query[2]).getOrDefault((query[1] - query[0] % query[2]) / query[2] + 1, 1L) * BigInteger.valueOf(query[3]).modInverse(BigInteger.valueOf(1000000007)).intValue() % 1000000007);
            }
        }
        for (int i = 1; i <= Math.sqrt(nums.length); i++) {
            for (int j = 0, prev = 0; j < i; j++) {
                long cur = 1;
                for (Map.Entry<Integer, Long> entry : diff.getOrDefault(i, new HashMap<>()).getOrDefault(j, new TreeMap<>()).entrySet()) {
                    for (int p = prev; p < entry.getKey() && j + p * i < nums.length; p++) {
                        mul[j + p * i] = mul[j + p * i] * cur % 1000000007;
                    }
                    cur = cur * entry.getValue() % 1000000007;
                    prev = entry.getKey();
                }
                for (int k = prev; j + k * i < nums.length; k++) {
                    mul[j + k * i] = mul[j + k * i] * cur % 1000000007;
                }
            }
        }
        int result = 0;
        for (int i = 0; i < nums.length; i++) {
            result ^= nums[i] * mul[i] % 1000000007;
        }
        return result;
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/