"""
Задача A. Lever (Codeforces 2131)

Во вселенной Divergent, The Lever выполняет итерации с двумя массивами a и b длины n. 
В каждой итерации Lever выполняет следующие шаги:

1. Выбирает случайный индекс i, такой что a[i] > b[i], и уменьшает a[i] на 1.
2. Выбирает случайный индекс i, такой что a[i] < b[i], и увеличивает a[i] на 1.

Итерация завершается, если шаг 1 был проигнорирован.

Ваша задача — найти количество итераций, которые выполнит Lever, чтобы массив a стал равным массиву b.

Входные данные:
- t (1 ≤ t ≤ 10^4) — количество тестов.
- Для каждого теста:
  - n (1 ≤ n ≤ 10) — длина массивов.
  - Массив a длины n.
  - Массив b длины n.

Выходные данные:
- Для каждого теста выведите одно число — количество итераций.

Пример:
Вход:
4
2
7 3
5 6
3
3 1 4
3 1 4
1
10
1
6
1 1 4 5 1 4
1 9 1 9 8 1

Выход:
3
1
10
7
"""

def count_iterations(n, a, b):
    """
    Подсчитывает количество итераций, которые выполняет Рычаг,
    преобразуя массив a в массив b согласно правилам задачи.

    На каждой итерации:
    1. Если есть индекс i с a[i] > b[i], уменьшаем a[i] на 1.
       Если таких индексов нет, шаг пропускается.
    2. Если есть индекс i с a[i] < b[i], увеличиваем a[i] на 1.
       Если таких индексов нет, шаг пропускается.
    Итерация считается выполненной, даже если первый шаг был пропущен,
    но после такой итерации процесс завершается.

    Args:
        n (int): длина массивов a и b.
        a (list[int]): исходный массив.
        b (list[int]): целевой массив.

    Returns:
        int: количество выполненных итераций.
    """
    a = a[:]  # копия массива
    iterations = 0

    while True:
        idx_dec = next((i for i in range(n) if a[i] > b[i]), None)
        if idx_dec is None:
            # Шаг 1 пропущен — считаем эту итерацию и завершаем процесс
            iterations += 1
            break

        a[idx_dec] -= 1

        idx_inc = next((i for i in range(n) if a[i] < b[i]), None)
        if idx_inc is not None:
            a[idx_inc] += 1

        iterations += 1

    return iterations


def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        print(count_iterations(n, a, b))


if __name__ == "__main__":
    main()

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks