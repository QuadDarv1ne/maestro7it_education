/*
https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

import java.util.*;

class Solution {
    public int[] successfulPairs(int[] spells, int[] potions, long success) {
        Arrays.sort(potions);
        int m = potions.length;
        int n = spells.length;
        int[] ans = new int[n];
        for (int i = 0; i < n; i++) {
            int spell = spells[i];
            long req = (success + spell - 1) / spell;
            int idx = firstGreaterOrEqual(potions, req);
            ans[i] = m - idx;
        }
        return ans;
    }

    // Возвращает первый индекс j в potions, где potions[j] >= target
    private int firstGreaterOrEqual(int[] potions, long target) {
        int l = 0, r = potions.length;
        while (l < r) {
            int mid = l + (r - l) / 2;
            if ((long)potions[mid] >= target) {
                r = mid;
            } else {
                l = mid + 1;
            }
        }
        return l;
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
*/