'''
https://coderun.yandex.ru/selections/yandex-interview/problems/generating-bracket-sequences
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

# Увеличиваем лимит рекурсии на случай больших n (хотя для n<=10 стандартного хватает)
sys.setrecursionlimit(10000)


def generate_sequences(n, s, open_count, close_count, result):
    """
    Рекурсивная функция для генерации правильных скобочных последовательностей.
    
    :param n: общее количество пар скобок
    :param s: текущая строка
    :param open_count: количество уже открытых скобок
    :param close_count: количество уже закрытых скобок
    :param result: список для сохранения результатов
    """
    # Базовый случай: если длина строки равна 2*n, мы сформировали полную последовательность
    if len(s) == 2 * n:
        result.append(s)
        return
    
    # Мы можем добавить открывающую скобку, если их меньше n
    if open_count < n:
        generate_sequences(n, s + '(', open_count + 1, close_count, result)
        
    # Мы можем добавить закрывающую скобку, если их меньше, чем открытых
    if close_count < open_count:
        generate_sequences(n, s + ')', open_count, close_count + 1, result)


def main():
    """
    Решение задачи "Генерация скобочных последовательностей" с Yandex CodeRun.
    На вход подается число n (1 <= n <= 10). 
    Необходимо вывести все правильные скобочные последовательности длины 2n 
    в лексикографическом порядке (каждую на новой строке).
    
    Пример ввода:
    3
    
    Пример вывода:
    ((()))
    (()())
    (())()
    ()(())
    ()()()
    """
    # Читаем все данные, избавляясь от лишних пробелов и переносов строк
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    result = []
    
    # Запускаем генерацию
    if n > 0:
        generate_sequences(n, "", 0, 0, result)
    
    # Выводим результат, каждый элемент с новой строки
    # Использование join работает быстрее, чем множественный вызов print
    sys.stdout.write('\n'.join(result))
    if result:
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
