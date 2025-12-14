'''
https://leetcode.com/problems/count-mentions-per-user/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def countMentions(self, numberOfUsers, events):
        """
        Решение задачи "Count Mentions Per User" (LeetCode 3433).

        Идея:
        - Сортировка по timestamp с OFFLINE перед MESSAGE.
        - Отслеживаем, когда пользователи снова онлайн.
        - Обрабатываем каждое MESSAGE в соответствии с token-ами ("ALL", "HERE" или "id<number>").
        """

        # Сортируем: сначала по времени, затем так, чтобы OFFLINE предшествовал MESSAGE
        events.sort(key=lambda e: (int(e[1]), 0 if e[0] == "OFFLINE" else 1))

        mentions = [0] * numberOfUsers
        # По каждому пользователю, до какого времени он офлайн
        offline_until = [0] * numberOfUsers

        for typ, ts, data in events:
            t = int(ts)
            # Обновляем статус онлайн для всех
            for i in range(numberOfUsers):
                # Если время offline_until[i] прошло — ставим онлайн
                if offline_until[i] <= t:
                    offline_until[i] = 0

            if typ == "OFFLINE":
                user_id = int(data)
                # Пользователь офлайн до t + 60
                offline_until[user_id] = t + 60

            else:  # MESSAGE
                if data == "ALL":
                    # Упоминаем всех, даже офлайн
                    for i in range(numberOfUsers):
                        mentions[i] += 1

                elif data == "HERE":
                    # Упоминаем только тех, кто сейчас онлайн
                    for i in range(numberOfUsers):
                        if offline_until[i] == 0:
                            mentions[i] += 1

                else:
                    # Явные id-упоминания, возможно несколько
                    for token in data.split():
                        if token.startswith("id"):
                            uid = int(token[2:])
                            mentions[uid] += 1

        return mentions
