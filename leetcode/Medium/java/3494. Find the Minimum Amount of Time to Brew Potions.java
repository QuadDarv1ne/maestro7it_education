/*
https://leetcode.com/problems/find-the-minimum-amount-of-time-to-brew-potions/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

import java.util.*;

class Solution {
    public long minTime(int[] skill, int[] mana) {
        if (skill.length == 0 || mana.length == 0) return 0;
        long sumSkill = 0;
        for (int s : skill) sumSkill += s;
        long prevWizardDone = sumSkill * (long)mana[0];
        for (int j = 1; j < mana.length; ++j) {
            long prevPotionDone = prevWizardDone;
            for (int i = skill.length - 2; i >= 0; --i) {
                prevPotionDone -= (long)skill[i + 1] * mana[j - 1];
                prevWizardDone = Math.max(prevPotionDone,
                                          prevWizardDone - (long)skill[i] * mana[j]);
            }
            prevWizardDone += sumSkill * (long)mana[j];
        }
        return prevWizardDone;
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