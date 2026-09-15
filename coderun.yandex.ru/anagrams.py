'''
https://coderun.yandex.ru/selections/yandex-interview/problems/anagrams
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
'''

import sys

def main():
    """
    Решение задачи "Анаграммы" с Yandex CodeRun.
    Оптимизировано по памяти: использует массив счетчиков и потоковую обработку.
    """
    # Читаем первую строку
    s1 = sys.stdin.readline().strip()
    # Читаем вторую строку
    s2 = sys.stdin.readline().strip()
    
    # Быстрая проверка: разные длины -> не анаграммы
    if len(s1) != len(s2):
        print(0)
        return
    
    # Массив счетчиков для 26 строчных латинских букв
    count = [0] * 26
    
    # Подсчитываем символы в первой строке
    for char in s1:
        count[ord(char) - ord('a')] += 1
    
    # Вычитаем символы второй строки на лету
    for char in s2:
        idx = ord(char) - ord('a')
        count[idx] -= 1
        # Если счетчик стал отрицательным, во второй строке больше таких символов
        if count[idx] < 0:
            print(0)
            return
    
    # Если все счетчики обнулились, строки являются анаграммами
    print(1)

if __name__ == '__main__':
    main()
