'''
https://leetcode.com/problems/find-the-minimum-amount-of-time-to-brew-potions/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution(object):
    def minTime(self, skill, mana):
        """
        Решение LeetCode 3494: Find the Minimum Amount of Time to Brew Potions.

        Идея:
        - sumSkill = сумма скоростей всех волшебников.
        - prevWizardDone — текущее минимальное время, к которому успел "догнать"
          последний (n-1)-й волшебник для предыдущих обработанных зелий.
        - При обработке следующего зелья j используем вспомогательную величину
          prevPotionDone и проходим волшебников справа налево, корректируя
          prevWizardDone так, чтобы обеспечить согласованность (передача сразу).
        - Итог — prevWizardDone после всех зелий.

        Сложность: O(n * m), память O(1).
        """
        if not skill or not mana:
            return 0
        sumSkill = sum(skill)
        # Время для первого зелья (последний волшебник завершит в sumSkill * mana[0])
        prevWizardDone = sumSkill * mana[0]
        for j in range(1, len(mana)):
            prevPotionDone = prevWizardDone
            # идём от предпоследнего волшебника к первому
            for i in range(len(skill) - 2, -1, -1):
                # снимаем вклад времени, связанный с предыдущим зельем у волшебника i+1
                prevPotionDone -= skill[i + 1] * mana[j - 1]
                # максимум между:
                #  - prevPotionDone (раннее доступное время, чтобы не нарушать порядок)
                #  - prevWizardDone - time_i_for_current_potion (ограничение по времени старта)
                prevWizardDone = max(prevPotionDone, prevWizardDone - skill[i] * mana[j])
            # добавляем время суммарной работы всех волшебников для текущего зелья
            prevWizardDone += sumSkill * mana[j]
        return prevWizardDone

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
