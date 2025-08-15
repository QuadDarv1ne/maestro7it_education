/**
 * https://leetcode.com/problems/top-k-frequent-elements/
 */

using System.Collections.Generic;
public class Solution {
    public int[] TopKFrequent(int[] nums, int k) {
        var cnt = new Dictionary<int,int>();
        foreach (int x in nums) cnt[x] = cnt.GetValueOrDefault(x, 0) + 1;
        var buckets = new List<int>[nums.Length + 1];
        for (int i = 0; i < buckets.Length; i++) buckets[i] = new List<int>();
        foreach (var kv in cnt) buckets[kv.Value].Add(kv.Key);
        var res = new List<int>();
        for (int f = buckets.Length - 1; f >= 0 && res.Count < k; --f)
            res.AddRange(buckets[f]);
        return res.GetRange(0, k).ToArray();
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