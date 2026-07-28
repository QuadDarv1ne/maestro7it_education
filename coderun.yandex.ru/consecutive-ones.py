'''
https://coderun.yandex.ru/selections/yandex-interview/problems/consecutive-ones
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
    Решение задачи "Максимальное количество подряд идущих единиц" (Consecutive Ones).
    На вход подается число n — количество элементов массива, и затем n чисел (0 или 1).
    Необходимо найти максимальное количество подряд идущих единиц.
    
    Пример ввода:
    6
    1 1 0 1 1 1
    
    Пример вывода:
    3
    """
    # Читаем все данные из стандартного ввода и разбиваем по пробелам/переносам строк
    data = sys.stdin.read().split()
    if not data:
        return
    
    # Первое число — размер массива
    n = int(data[0])
    
    # Извлекаем элементы массива (берем ровно n элементов, начиная со второго)
    arr = data[1:n+1] if len(data) > n else data[1:]
    
    max_streak = 0
    current_streak = 0
    
    # Проходим по всем элементам массива
    for val in arr:
        if val == '1':
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            current_streak = 0
            
    print(max_streak)


if __name__ == '__main__':
    main()
