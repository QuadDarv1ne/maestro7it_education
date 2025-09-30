'''
https://codeforces.com/contest/2139/problem/C

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

from collections import Counter

def can_form_palindrome(s: str) -> str:
    """
    Функция проверяет, можно ли переставить символы строки s так,
    чтобы она стала палиндромом.

    :param s: Строка длины n (1 ≤ n ≤ 1000).
    :return: "YES", если строку можно переставить в палиндром, и "NO" в противном случае.
    """
    # Подсчитываем количество вхождений каждого символа
    freq = Counter(s)
    
    # Подсчитываем количество символов с нечётной частотой
    odd_count = sum(1 for count in freq.values() if count % 2 != 0)
    
    # Если строка чётной длины, все символы должны встречаться чётное количество раз
    # Если строка нечётной длины, только один символ может встречаться нечётное количество раз
    if odd_count > 1:
        return "NO"
    return "YES"

# Пример использования
if __name__ == "__main__":
    t = int(input())  # Количество тестов
    for _ in range(t):
        s = input().strip()  # Ввод строки
        print(can_form_palindrome(s))

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks