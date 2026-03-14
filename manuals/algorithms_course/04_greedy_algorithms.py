"""
ЖАДНЫЕ АЛГОРИТМЫ (GREEDY ALGORITHMS)

Условие применения:
Задача, где локально оптимальный выбор на каждом шаге приводит к глобальному оптимуму.

Суть метода:
"Бери лучшее прямо сейчас" — на каждом шаге выбираем вариант, который кажется
наилучшим в данный момент, без пересмотра предыдущих решений.

Сложность: обычно O(n) или O(n log n) — значительно быстрее, чем полный перебор.

Важно:
Жадный алгоритм НЕ всегда даёт оптимальное решение!
Для оптимальности нужны два свойства:
1. Жадный выбор: локальный оптимум ведёт к глобальному
2. Оптимальная подструктура: решение подзадач оптимально для всей задачи

Когда работает:
- Задача о выборе интервалов
- Дробная задача о рюкзаке (но НЕ классическая!)
- Размен монет с "хорошими" номиналами (1, 2, 5, 10...)
- Кодирование Хаффмана
- Алгоритм Дейкстры (кратчайшие пути)

Когда НЕ работает:
- Классическая задача о рюкзаке
- Размен монет с произвольными номиналами (пример: [1, 3, 4], сумма 6)
"""


def coin_change_greedy(amount, coins=None):
    """
    Жадный алгоритм размена монет.
    
    ВНИМАНИЕ: Работает только для "канонических" систем номиналов!
    Примеры канонических: рубли/USD (1, 2, 5, 10, ...), евроценты
    
    Аргументы:
        amount: сумма для размена
        coins: список номиналов монет (по умолчанию [1, 2, 5, 10])
    
    Возвращает:
        int: минимальное количество монет
    
    Сложность: O(n log n) из-за сортировки, O(n) без учёта сортировки
    
    Пример:
        >>> coin_change_greedy(73, [1, 2, 5, 10])
        9
    """
    if coins is None:
        coins = [1, 2, 5, 10]
    
    coins = sorted(coins, reverse=True)  # Начинаем с крупных
    count = 0
    remaining = amount
    
    for coin in coins:
        if remaining <= 0:
            break
        num_coins = remaining // coin
        count += num_coins
        remaining -= num_coins * coin
        if num_coins > 0:
            print(f"  Взято {num_coins} монет(а) по {coin}")
    
    return count if remaining == 0 else -1


def activity_selection(intervals):
    """
    Задача о выборе максимального числа непересекающихся интервалов.
    
    Классический пример, где жадный алгоритм оптимален!
    Стратегия: всегда выбирать интервал с самым ранним окончанием.
    
    Аргументы:
        intervals: список кортежей (start, end)
    
    Возвращает:
        list: максимальный набор непересекающихся интервалов
    
    Сложность: O(n log n) из-за сортировки
    
    Пример:
        >>> intervals = [(1, 3), (2, 5), (4, 6), (6, 8)]
        >>> activity_selection(intervals)
        [(1, 3), (4, 6), (6, 8)]
    """
    if not intervals:
        return []
    
    # Сортируем по времени окончания
    intervals = sorted(intervals, key=lambda x: x[1])
    
    selected = [intervals[0]]
    last_end = intervals[0][1]
    
    for start, end in intervals[1:]:
        if start >= last_end:  # Интервал не пересекается
            selected.append((start, end))
            last_end = end
    
    return selected


def fractional_knapsack(items, capacity):
    """
    Дробная задача о рюкзаке.
    
    Можно брать части предметов. Жадный алгоритм оптимален!
    Стратегия: брать предметы в порядке убывания ценности на единицу веса.
    
    Аргументы:
        items: список кортежей (weight, value)
        capacity: вместимость рюкзака
    
    Возвращает:
        float: максимальная ценность
    
    Сложность: O(n log n) из-за сортировки
    
    Пример:
        >>> items = [(10, 60), (20, 100), (30, 120)]
        >>> fractional_knapsack(items, 50)
        240.0
    """
    # Сортируем по убыванию отношения ценность/вес
    items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    
    total_value = 0
    remaining = capacity
    
    for weight, value in items:
        if remaining >= weight:
            # Берём предмет целиком
            total_value += value
            remaining -= weight
            print(f"  Взят предмет целиком: вес={weight}, ценность={value}")
        else:
            # Берём часть предмета
            fraction = remaining / weight
            total_value += value * fraction
            print(f"  Взят предмет частично: {fraction*100:.1f}%, ценность={value*fraction}")
            break
    
    return total_value


def jump_game(nums):
    """
    Задача о прыжках: можно ли добраться до последнего индекса?
    
    nums[i] = максимальная длина прыжка от позиции i.
    Жадная стратегия: поддерживаем максимальную достижимую позицию.
    
    Аргументы:
        nums: список максимальных длин прыжков
    
    Возвращает:
        bool: True если можно добраться до конца
    
    Сложность: O(n)
    
    Пример:
        >>> jump_game([2, 3, 1, 1, 4])
        True
        >>> jump_game([3, 2, 1, 0, 4])
        False
    """
    max_reach = 0
    
    for i, jump in enumerate(nums):
        if i > max_reach:  # Позиция недостижима
            return False
        max_reach = max(max_reach, i + jump)
        if max_reach >= len(nums) - 1:
            return True
    
    return True


def jump_game_min_jumps(nums):
    """
    Минимальное количество прыжков для достижения конца.
    
    Аргументы:
        nums: список максимальных длин прыжков
    
    Возвращает:
        int: минимальное количество прыжков
    
    Сложность: O(n)
    
    Пример:
        >>> jump_game_min_jumps([2, 3, 1, 1, 4])
        2
    """
    if len(nums) <= 1:
        return 0
    
    jumps = 0
    current_end = 0  # Граница текущего прыжка
    farthest = 0     # Самая дальняя достижимая позиция
    
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        
        if i == current_end:  # Нужно совершить прыжок
            jumps += 1
            current_end = farthest
    
    return jumps


def gas_station_circuit(gas, cost):
    """
    Задача о газовой станции.
    
    Есть круговой маршрут с N станциями. gas[i] = запас бензина,
    cost[i] = расход до следующей станции.
    Найти стартовую станцию для полного круга, или -1 если невозможно.
    
    Аргументы:
        gas: список запасов бензина
        cost: список расходов
    
    Возвращает:
        int: индекс стартовой станции или -1
    
    Сложность: O(n)
    
    Пример:
        >>> gas_station_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
        3
    """
    total_gas = sum(gas)
    total_cost = sum(cost)
    
    if total_gas < total_cost:
        return -1  # Решение невозможно
    
    start = 0
    current_gas = 0
    
    for i in range(len(gas)):
        current_gas += gas[i] - cost[i]
        
        if current_gas < 0:
            # Не можем начать с текущей позиции — пробуем следующую
            start = i + 1
            current_gas = 0
    
    return start


def candy_distribution(ratings):
    """
    Задача о распределении конфет.
    
    Каждый ребёнок должен получить минимум 1 конфету.
    Ребёнок с бóльшим рейтингом получает больше конфет, чем соседи.
    
    Аргументы:
        ratings: список рейтингов детей
    
    Возвращает:
        int: минимальное общее количество конфет
    
    Сложность: O(n)
    
    Пример:
        >>> candy_distribution([1, 0, 2])
        5
    """
    n = len(ratings)
    candies = [1] * n
    
    # Проход слева направо
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    
    # Проход справа налево
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    
    return sum(candies)


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*50)
    
    # Демонстрация размена монет
    print("Размен 73 рублей:")
    print(f"Итого монет: {coin_change_greedy(73)}")
    
    # Демонстрация выбора интервалов
    print("\nВыбор интервалов:")
    intervals = [(1, 3), (2, 5), (4, 6), (6, 8), (5, 7)]
    print(f"Интервалы: {intervals}")
    print(f"Выбрано: {activity_selection(intervals)}")
    
    # Демонстрация дробного рюкзака
    print("\nДробный рюкзак (вместимость 50):")
    items = [(10, 60), (20, 100), (30, 120)]
    print(f"Предметы (вес, ценность): {items}")
    print(f"Максимальная ценность: {fractional_knapsack(items, 50)}")
