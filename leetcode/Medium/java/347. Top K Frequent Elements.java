/**
 * https://leetcode.com/problems/top-k-frequent-elements/
 */

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int n : nums) count.put(n, count.getOrDefault(n, 0) + 1);
        List<Integer>[] buckets = new ArrayList[nums.length + 1];
        for (int i = 0; i <= nums.length; i++) buckets[i] = new ArrayList<>();
        for (Map.Entry<Integer, Integer> e : count.entrySet()) {
            buckets[e.getValue()].add(e.getKey());
        }
        List<Integer> res = new ArrayList<>();
        for (int i = buckets.length - 1; i >= 0 && res.size() < k; i--) {
            res.addAll(buckets[i]);
        }
        return res.stream().limit(k).mapToInt(Integer::intValue).toArray();
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