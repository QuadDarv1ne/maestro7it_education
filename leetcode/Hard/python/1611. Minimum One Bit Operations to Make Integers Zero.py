'''
https://leetcode.com/problems/minimum-one-bit-operations-to-make-integers-zero/description/?envType=daily-question&envId=2025-11-08
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
'''

class Solution(object):
    def minimumOneBitOperations(self, n):
        """
        :type n: int
        :rtype: int
        """
        # Ключевая идея: количество операций для числа n равно n XOR (n >> 1) XOR (n >> 2) XOR ...
        # Это преобразование из обычного двоичного кода в код Грея (Gray code)
        # Код Грея показывает минимальное число операций для достижения 0
        
        result = 0
        while n:
            result ^= n
            n >>= 1
        
        return result

''' 
Альтернативное решение через рекурсию с мемоизацией:

class Solution(object):
    def minimumOneBitOperations(self, n):
        memo = {}
        
        def solve(num):
            if num == 0:
                return 0
            if num in memo:
                return memo[num]
            
            # Находим позицию старшего бита
            msb = 0
            temp = num
            while temp:
                temp >>= 1
                msb += 1
            msb -= 1
            
            # Формула: f(n) = 2^(msb+1) - 1 - f(n XOR 2^msb)
            result = (1 << (msb + 1)) - 1 - solve(num ^ (1 << msb))
            memo[num] = result
            return result
        
        return solve(n)

Объяснение:
1. Задача связана с кодом Грея - системой счисления, где соседние числа отличаются на 1 бит
2. Количество операций для преобразования n в 0 равно обратному коду Грея числа n
3. Обратный код Грея вычисляется как: result = n XOR (n>>1) XOR (n>>2) XOR ...
4. Это самый эффективный способ: O(log n) по времени, O(1) по памяти

Примеры:
- n = 3 (011): 3 XOR 1 = 2
- n = 6 (110): 6 XOR 3 XOR 1 = 4
'''

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks