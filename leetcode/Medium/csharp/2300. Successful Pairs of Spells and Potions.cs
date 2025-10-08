/*
https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

using System;
using System.Collections.Generic;

public class Solution {
    public int[] SuccessfulPairs(int[] spells, int[] potions, long success) {
        Array.Sort(potions);
        int m = potions.Length;
        int n = spells.Length;
        int[] ans = new int[n];
        for (int i = 0; i < n; i++) {
            int spell = spells[i];
            long req = (success + spell - 1) / spell;
            int idx = FirstGE(potions, req);
            ans[i] = m - idx;
        }
        return ans;
    }

    // бинарный поиск: первый индекс, где potions[idx] >= target
    private int FirstGE(int[] arr, long target) {
        int l = 0, r = arr.Length;
        while (l < r) {
            int mid = l + (r - l) / 2;
            if (arr[mid] >= target) {
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