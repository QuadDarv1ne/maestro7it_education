'''
Решение задачи: https://itresume.ru/problems/sber-prime-factorization
'''

class Answer:
    """
    Автор: Дуплей Максим Игоревич
    ORCID: https://orcid.org/0009-0007-7605-539X
    GitHub: https://github.com/QuadDarv1ne/

    Класс Answer содержит метод decomp, который разлагает факториал числа n
    на простые множители и возвращает строковое представление в формате:
    "a^b * c^d * ... * e", где a, c, ... — простые числа в порядке возрастания,
    а b, d, ... — соответствующие показатели степени. Если показатель степени
    равен 1, он не указывается.

    Методы:
    - decomp(n): возвращает строку разложения факториала n на простые множители.
    - sieve_of_eratosthenes(n): возвращает список всех простых чисел до n включительно.
    """

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

'''
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''
