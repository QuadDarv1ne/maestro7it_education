"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Solution:
    def countPrimes(self, n):
        if n <= 2:
            return 0
        
        # Инициализируем массив, все числа считаем простыми
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False
        
        # Проверяем до квадратного корня из n
        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                # Отмечаем кратные числа как составные
                for j in range(i * i, n, i):
                    is_prime[j] = False
        
        # Считаем простые числа
        return sum(is_prime)