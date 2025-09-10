'''
https://leetcode.com/problems/minimum-number-of-people-to-teach/description/?envType=daily-question&envId=2025-09-10
'''

class Solution:
    def minimumTeachings(self, n, languages, friendships):
        """
        Найти минимальное число людей, которым нужно преподать один язык,
        чтобы все друзья могли общаться (имели хотя бы один общий язык).
        Жадный выбор: выбрать язык, который максимально известен среди
        проблемных пользователей, и обучить остальных.
        """
        # Найти проблемные дружбы и собрать проблемных пользователей
        bad = set()
        for u, v in friendships:
            if not set(languages[u - 1]).intersection(languages[v - 1]):
                bad.add(u - 1)
                bad.add(v - 1)
        if not bad:
            return 0
        # Считаем, кто какой язык знает
        cnt = [0] * (n + 1)
        for u in bad:
            for lang in languages[u]:
                cnt[lang] += 1
        # Выбираем язык с максимальным покрытием
        max_known = max(cnt)
        return len(bad) - max_known

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks