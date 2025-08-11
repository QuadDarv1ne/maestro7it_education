/**
 * https://leetcode.com/problems/minimum-genetic-mutation/description/?envType=study-plan-v2&envId=top-interview-150
 */

import java.util.*;

class Solution {
    public int minMutation(String startGene, String endGene, String[] bank) {
        Set<String> bankSet = new HashSet<>(Arrays.asList(bank));
        if (!bankSet.contains(endGene)) {
            return -1;
        }

        Queue<Pair<String, Integer>> queue = new LinkedList<>();
        queue.offer(new Pair<>(startGene, 0));

        while (!queue.isEmpty()) {
            Pair<String, Integer> pair = queue.poll();
            String gene = pair.getKey();
            int level = pair.getValue();

            char[] chars = gene.toCharArray();
            for (int i = 0; i < chars.length; i++) {
                char original = chars[i];
                for (char c : new char[]{'A', 'C', 'G', 'T'}) {
                    chars[i] = c;
                    String nextGene = new String(chars);
                    if (nextGene.equals(endGene)) {
                        return level + 1;
                    }
                    if (bankSet.contains(nextGene)) {
                        bankSet.remove(nextGene);
                        queue.offer(new Pair<>(nextGene, level + 1));
                    }
                }
                chars[i] = original;
            }
        }

        return -1;
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