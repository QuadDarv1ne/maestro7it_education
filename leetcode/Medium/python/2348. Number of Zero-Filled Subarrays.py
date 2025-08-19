'''
https://leetcode.com/problems/number-of-zero-filled-subarrays/description/?envType=daily-question&envId=2025-08-19
'''

# from typing import List

class Solution:
    # def zeroFilledSubarray(self, nums: List[int]) -> int:
    def zeroFilledSubarray(self, nums):
        """
        Подсчитывает количество непрерывных подмассивов, полностью состоящих из нулей.

        Идея:
        Проходим по массиву, поддерживаем текущую длину подряд идущих нулей `cnt`.
        При встрече нуля увеличиваем `cnt` и добавляем его в ответ `ans`.
        Это эквивалентно сумме 1+2+...+k для каждого сегмента нулей длины k.

        Время: O(n), Память: O(1)

        Пример:
        nums = [1,3,0,0,2,0,0,4] -> возвращает 6
        """
        ans = 0
        cnt = 0
        for x in nums:
            if x == 0:
                cnt += 1
                ans += cnt
            else:
                cnt = 0
        return ans

# Простой тест при запуске в локальной среде
if __name__ == "__main__":
    example = [1,3,0,0,2,0,0,4]
    print(Solution().zeroFilledSubarray(example))  # Ожидаемый вывод: 6

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks