'''
https://itresume.ru/problems/sber-prime-factorization
'''

class Answer:
    def decomp(self, n):
        primes = self.sieve_of_eratosthenes(n)
        result = []
        for p in primes:
            count = 0
            power = p
            while power <= n:
                count += n // power
                power *= p
            if count > 0:
                if count == 1:
                    result.append(f"{p}")
                else:
                    result.append(f"{p}^{count}")
        return " * ".join(result)

    def sieve_of_eratosthenes(self, n):
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        for start in range(2, int(n**0.5) + 1):
            if sieve[start]:
                for i in range(start*start, n + 1, start):
                    sieve[i] = False
        return [num for num, is_prime in enumerate(sieve) if is_prime]

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
