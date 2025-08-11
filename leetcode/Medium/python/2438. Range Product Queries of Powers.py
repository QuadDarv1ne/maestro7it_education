'''
# Функция productQueries:
# @param n — исходное число, разбивается на степени двойки.
# @param queries — вектор запросов [l, r].
# @return вектор ответов — произведения степеней двойки в диапазоне по модулю 1e9+7.

# Подход:
# 1. Извлекаем set-биты n, формируя массив степеней двойки.
# 2. Строим префиксный массив накопленных произведений mod.
# 3. Для запроса используем modular inverse (быстрое возведение в степень).
'''

MOD = 10**9 + 7

class Solution:
    def productQueries(self, n, queries):
        # Извлекаем степени двойки, входящие в разложение числа n
        powers = []
        for i in range(32):
            if n & (1 << i):
                powers.append(1 << i)

        # Строим префиксный массив произведений степеней двойки по модулю
        prefix = [1]
        for p in powers:
            prefix.append((prefix[-1] * p) % MOD)

        result = []
        for l, r in queries:
            # Используем свойство: произведение от l до r
            # = prefix[r+1] * modular_inverse(prefix[l]) mod MOD
            inv = pow(prefix[l], MOD - 2, MOD)
            product = (prefix[r + 1] * inv) % MOD
            result.append(product)

        return result

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks