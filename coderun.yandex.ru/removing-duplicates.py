'''
https://coderun.yandex.ru/selections/yandex-interview/problems/removing-duplicates
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
    Решение задачи "Удаление дубликатов" с Yandex CodeRun.
    На вход подается массив строк или чисел. Необходимо удалить из него все дубликаты,
    оставив только первое вхождение каждого элемента, и вывести результат.
    """
    # Читаем все данные из стандартного ввода, разбивая по пробелам и переносам строк
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # Универсальная обработка ввода:
    # Часто в задачах Яндекса первым элементом идет число N (количество элементов).
    # Если первое слово - это число, и оно равно количеству оставшихся элементов,
    # то считаем его размером массива и отбрасываем.
    if input_data[0].isdigit() and len(input_data) == int(input_data[0]) + 1:
        elements = input_data[1:]
    else:
        elements = input_data
        
    seen = set()
    result = []
    
    # Проходим по всем элементам и оставляем только первые вхождения
    for item in elements:
        if item not in seen:
            seen.add(item)
            result.append(item)
            
    # Выводим результат через пробел
    sys.stdout.write(' '.join(result) + '\n')


if __name__ == '__main__':
    main()
