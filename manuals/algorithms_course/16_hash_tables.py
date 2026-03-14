"""
ХЕШ-ТАБЛИЦЫ И МНОЖЕСТВА (HASH TABLES AND SETS)

Хеш-таблица — это структура данных, реализующая интерфейс ассоциативного массива.
Она позволяет хранить пары ключ-значение и выполнять операции поиска, вставки
и удаления в среднем за O(1).

Основные понятия:
- Хеш-функция: преобразует ключ в индекс массива
- Коллизия: ситуация, когда два ключа дают одинаковый хеш
- Разрешение коллизий: chaining (цепочки) или open addressing (открытая адресация)

В Python:
- dict — хеш-таблица для пар ключ-значение
- set — хеш-таблица только для ключей

Сложность операций:
- Поиск: O(1) среднее, O(n) худшее
- Вставка: O(1) среднее, O(n) худшее
- Удаление: O(1) среднее, O(n) худшее

Важно: худший случай возникает при большом количестве коллизий
"""

from typing import List, Dict, Set, Optional
from collections import defaultdict, Counter


# ===== СОБСТВЕННАЯ РЕАЛИЗАЦИЯ ХЕШ-ТАБЛИЦЫ =====

class HashMap:
    """
    Собственная реализация хеш-таблицы с цепочками.
    
    Использует метод chaining для разрешения коллизий.
    Каждый бакет содержит список пар (key, value).
    
    Пример:
        >>> hm = HashMap()
        >>> hm.put("key1", "value1")
        >>> hm.get("key1")
        'value1'
    """
    
    def __init__(self, capacity: int = 16):
        """
        Инициализация хеш-таблицы.
        
        Аргументы:
            capacity: начальное количество бакетов
        """
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
        self.load_factor = 0.75  # Порог для расширения
    
    def _hash(self, key) -> int:
        """
        Вычисление хеша ключа.
        
        Использует встроенную функцию hash() и берёт модуль.
        """
        return hash(key) % self.capacity
    
    def _resize(self):
        """Расширение таблицы при достижении порога загрузки."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        # Перехеширование всех элементов
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def put(self, key, value) -> None:
        """
        Вставка или обновление пары ключ-значение.
        
        Сложность: O(1) среднее
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Проверяем, существует ли ключ
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Обновление
                return
        
        # Добавляем новую пару
        bucket.append((key, value))
        self.size += 1
        
        # Проверяем необходимость расширения
        if self.size >= self.capacity * self.load_factor:
            self._resize()
    
    def get(self, key, default=None):
        """
        Получение значения по ключу.
        
        Сложность: O(1) среднее
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return default
    
    def remove(self, key) -> bool:
        """
        Удаление пары по ключу.
        
        Возвращает:
            bool: True если ключ существовал
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        
        return False
    
    def contains(self, key) -> bool:
        """Проверка наличия ключа."""
        return self.get(key, None) is not None or key in [k for bucket in self.buckets for k, v in bucket]
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        items = []
        for bucket in self.buckets:
            for k, v in bucket:
                items.append(f"{k}: {v}")
        return "{" + ", ".join(items) + "}"


class HashSet:
    """
    Собственная реализация множества на хеш-таблице.
    
    Хранит только ключи без значений.
    """
    
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
    
    def _hash(self, value) -> int:
        return hash(value) % self.capacity
    
    def add(self, value) -> bool:
        """
        Добавление элемента.
        
        Возвращает:
            bool: True если элемент был добавлен (не существовал)
        """
        index = self._hash(value)
        bucket = self.buckets[index]
        
        if value in bucket:
            return False
        
        bucket.append(value)
        self.size += 1
        return True
    
    def remove(self, value) -> bool:
        """Удаление элемента."""
        index = self._hash(value)
        bucket = self.buckets[index]
        
        if value in bucket:
            bucket.remove(value)
            self.size -= 1
            return True
        
        return False
    
    def contains(self, value) -> bool:
        """Проверка наличия элемента."""
        index = self._hash(value)
        return value in self.buckets[index]
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        for bucket in self.buckets:
            for value in bucket:
                yield value


# ===== КЛАССИЧЕСКИЕ ЗАДАЧИ НА ХЕШ-ТАБЛИЦАХ =====

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Найти два числа, дающие заданную сумму.
    
    Классическая задача на хеш-таблицу.
    Для каждого числа проверяем, есть ли (target - num) в таблице.
    
    Аргументы:
        nums: список чисел
        target: целевая сумма
    
    Возвращает:
        list: индексы двух чисел или пустой список
    
    Сложность: O(n) по времени, O(n) по памяти
    
    Пример:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
    """
    seen = {}  # значение -> индекс
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []


def contains_duplicate(nums: List[int]) -> bool:
    """
    Проверка наличия дубликатов в массиве.
    
    Аргументы:
        nums: список чисел
    
    Возвращает:
        bool: True если есть дубликаты
    
    Сложность: O(n)
    
    Пример:
        >>> contains_duplicate([1, 2, 3, 1])
        True
    """
    seen = set()
    
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    
    return False


def contains_nearby_duplicate(nums: List[int], k: int) -> bool:
    """
    Проверка наличия дубликатов на расстоянии не более k.
    
    Аргументы:
        nums: список чисел
        k: максимальное расстояние между индексами
    
    Возвращает:
        bool: True если есть близкие дубликаты
    
    Сложность: O(n)
    """
    seen = {}  # значение -> последний индекс
    
    for i, num in enumerate(nums):
        if num in seen and i - seen[num] <= k:
            return True
        seen[num] = i
    
    return False


def find_missing_number(nums: List[int]) -> int:
    """
    Найти пропущенное число в диапазоне [0, n].
    
    Массив длины n содержит числа от 0 до n без одного числа.
    
    Аргументы:
        nums: список чисел
    
    Возвращает:
        int: пропущенное число
    
    Сложность: O(n)
    """
    n = len(nums)
    num_set = set(nums)
    
    for i in range(n + 1):
        if i not in num_set:
            return i
    
    return -1


# ===== ПОДСЧЁТ ЭЛЕМЕНТОВ =====

def majority_element(nums: List[int]) -> int:
    """
    Найти элемент, встречающийся более n/2 раз.
    
    Гарантируется, что такой элемент существует.
    
    Аргументы:
        nums: список чисел
    
    Возвращает:
        int: мажоритарный элемент
    
    Сложность: O(n)
    
    Пример:
        >>> majority_element([3, 2, 3])
        3
    """
    count = Counter(nums)
    n = len(nums)
    
    for num, freq in count.items():
        if freq > n // 2:
            return num
    
    return -1


def majority_element_boyer_moore(nums: List[int]) -> int:
    """
    Алгоритм Бойера-Мура для поиска мажоритарного элемента.
    
    Не использует дополнительную память!
    O(1) по памяти, O(n) по времени.
    """
    candidate = None
    count = 0
    
    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1
    
    return candidate


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    K наиболее часто встречающихся элементов.
    
    Аргументы:
        nums: список чисел
        k: количество элементов
    
    Возвращает:
        list: k самых частых элементов
    
    Сложность: O(n) с bucket sort
    
    Пример:
        >>> top_k_frequent([1, 1, 1, 2, 2, 3], 2)
        [1, 2]
    """
    # Подсчёт частот
    count = Counter(nums)
    
    # Bucket sort по частоте
    # buckets[i] = элементы с частотой i
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]
    
    for num, freq in count.items():
        buckets[freq].append(num)
    
    # Собираем результат
    result = []
    for i in range(n, 0, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            return result[:k]
    
    return result


# ===== ГРУППИРОВКА =====

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Группировка анаграмм.
    
    Анаграммы — строки с одинаковым набором символов.
    
    Аргументы:
        strs: список строк
    
    Возвращает:
        list: группы анаграмм
    
    Сложность: O(n × k log k), k — средняя длина строки
    
    Пример:
        >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    """
    groups = defaultdict(list)
    
    for s in strs:
        # Сортировка как ключ
        key = ''.join(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())


def group_anagrams_count(strs: List[str]) -> List[List[str]]:
    """
    Группировка анаграмм с подсчётом символов.
    
    O(n × k) вместо O(n × k log k).
    """
    groups = defaultdict(list)
    
    for s in strs:
        # Подсчёт символов как ключ
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        
        # Преобразуем в tuple (хешируемый)
        key = tuple(count)
        groups[key].append(s)
    
    return list(groups.values())


def find_duplicate_subtrees(root) -> List:
    """
    Найти все дублирующиеся поддеревья.
    
    Использует сериализацию поддеревьев как ключей.
    
    Сложность: O(n²) в худшем случае для сериализации
    """
    from collections import defaultdict
    
    result = []
    count = defaultdict(int)
    
    def serialize(node) -> str:
        """Сериализация поддерева."""
        if not node:
            return "#"
        
        # Построение уникального представления
        s = f"{node.val},{serialize(node.left)},{serialize(node.right)}"
        
        count[s] += 1
        
        # Если встретили второй раз — добавляем
        if count[s] == 2:
            result.append(node)
        
        return s
    
    serialize(root)
    return result


# ===== ПРЕФИКСНЫЕ СУММЫ С ХЕШ-ТАБЛИЦЕЙ =====

def subarray_sum(nums: List[int], k: int) -> int:
    """
    Количество подмассивов с суммой k.
    
    Использует префиксные суммы и хеш-таблицу.
    
    Аргументы:
        nums: список чисел
        k: целевая сумма
    
    Возвращает:
        int: количество подмассивов
    
    Сложность: O(n)
    
    Пример:
        >>> subarray_sum([1, 1, 1], 2)
        2
    """
    count = 0
    prefix_sum = 0
    # Сколько раз встретилась каждая префиксная сумма
    sum_count = defaultdict(int)
    sum_count[0] = 1  # Пустой префикс
    
    for num in nums:
        prefix_sum += num
        
        # Если (prefix_sum - k) встречалась, то есть подмассив с суммой k
        count += sum_count[prefix_sum - k]
        
        sum_count[prefix_sum] += 1
    
    return count


def find_max_length(nums: List[int]) -> int:
    """
    Максимальная длина подмассива с равным количеством 0 и 1.
    
    Заменяем 0 на -1 и ищем подмассив с суммой 0.
    
    Аргументы:
        nums: список из 0 и 1
    
    Возвращает:
        int: максимальная длина
    
    Сложность: O(n)
    """
    # сумма -> первый индекс
    first_index = {0: -1}
    max_len = 0
    current_sum = 0
    
    for i, num in enumerate(nums):
        current_sum += 1 if num == 1 else -1
        
        if current_sum in first_index:
            max_len = max(max_len, i - first_index[current_sum])
        else:
            first_index[current_sum] = i
    
    return max_len


def continuous_subarray_sum(nums: List[int], k: int) -> bool:
    """
    Проверка наличия подмассива длины ≥ 2 с суммой, кратной k.
    
    Аргументы:
        nums: список чисел
        k: делитель
    
    Возвращает:
        bool: True если такой подмассив есть
    
    Сложность: O(n)
    """
    # остаток -> первый индекс
    remainder_index = {0: -1}
    prefix_sum = 0
    
    for i, num in enumerate(nums):
        prefix_sum += num
        remainder = prefix_sum % k
        
        if remainder in remainder_index:
            if i - remainder_index[remainder] >= 2:
                return True
        else:
            remainder_index[remainder] = i
    
    return False


# ===== ВЫБОРКА ЭЛЕМЕНТОВ =====

def random_pick_index(nums: List[int]):
    """
    Случайный выбор индекса заданного значения.
    
    Алгоритм резервуарной выборки.
    O(n)预处理, O(1) выбор.
    """
    import random
    
    # Предварительная обработка: индексы для каждого значения
    indices = defaultdict(list)
    for i, num in enumerate(nums):
        indices[num].append(i)
    
    def pick(target: int) -> int:
        """Случайный индекс для target."""
        return random.choice(indices[target])
    
    return pick


def insert_delete_getrandom():
    """
    Структура данных с O(1) вставкой, удалением и случайным доступом.
    
    Комбинация хеш-таблицы и массива.
    """
    import random
    
    # массив значений
    values = []
    # значение -> индекс в массиве
    indices = {}
    
    def insert(val: int) -> bool:
        """Вставка. Возвращает False если уже существует."""
        if val in indices:
            return False
        
        indices[val] = len(values)
        values.append(val)
        return True
    
    def remove(val: int) -> bool:
        """Удаление. Возвращает False если не существует."""
        if val not in indices:
            return False
        
        # Меняем местами с последним элементом
        idx = indices[val]
        last_val = values[-1]
        
        values[idx] = last_val
        indices[last_val] = idx
        
        # Удаляем последний элемент
        values.pop()
        del indices[val]
        
        return True
    
    def get_random() -> int:
        """Случайный элемент."""
        return random.choice(values)
    
    return insert, remove, get_random


# ===== МНОЖЕСТВА =====

def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Пересечение двух массивов.
    
    Аргументы:
        nums1, nums2: массивы чисел
    
    Возвращает:
        list: общие элементы (без повторений)
    
    Сложность: O(n + m)
    """
    set1 = set(nums1)
    set2 = set(nums2)
    return list(set1 & set2)


def union(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Объединение двух массивов.
    
    Сложность: O(n + m)
    """
    return list(set(nums1) | set(nums2))


def difference(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Разность множеств (элементы nums1, не входящие в nums2).
    
    Сложность: O(n + m)
    """
    set2 = set(nums2)
    return [x for x in nums1 if x not in set2]


def is_disjoint(nums1: List[int], nums2: List[int]) -> bool:
    """
    Проверка отсутствия общих элементов.
    
    Сложность: O(n + m)
    """
    return set(nums1).isdisjoint(set(nums2))


# ===== ПОДСЧЁТ РАССТОЯНИЙ =====

def shortest_distance(words: List[str], word1: str, word2: str) -> int:
    """
    Минимальное расстояние между двумя словами в списке.
    
    Аргументы:
        words: список слов
        word1, word2: искомые слова
    
    Возвращает:
        int: минимальное расстояние
    
    Сложность: O(n)
    """
    index1 = -1
    index2 = -1
    min_dist = float('inf')
    
    for i, word in enumerate(words):
        if word == word1:
            index1 = i
            if index2 != -1:
                min_dist = min(min_dist, abs(index1 - index2))
        
        if word == word2:
            index2 = i
            if index1 != -1:
                min_dist = min(min_dist, abs(index1 - index2))
    
    return min_dist


# ===== УНИКАЛЬНОСТЬ =====

def is_isomorphic(s: str, t: str) -> bool:
    """
    Проверка изоморфности строк.
    
    Две строки изоморфны, если символы одной можно заменить,
    чтобы получить другую. Соответствие должно быть взаимно однозначным.
    
    Аргументы:
        s, t: строки
    
    Возвращает:
        bool: True если изоморфны
    
    Сложность: O(n)
    
    Пример:
        >>> is_isomorphic("egg", "add")
        True
        >>> is_isomorphic("foo", "bar")
        False
    """
    if len(s) != len(t):
        return False
    
    # Отображения в обе стороны
    s_to_t = {}
    t_to_s = {}
    
    for c1, c2 in zip(s, t):
        if c1 in s_to_t:
            if s_to_t[c1] != c2:
                return False
        else:
            s_to_t[c1] = c2
        
        if c2 in t_to_s:
            if t_to_s[c2] != c1:
                return False
        else:
            t_to_s[c2] = c1
    
    return True


def word_pattern(pattern: str, s: str) -> bool:
    """
    Проверка соответствия паттерна словам.
    
    Аргументы:
        pattern: паттерн из букв
        s: строка из слов
    
    Возвращает:
        bool: True если соответствует
    
    Пример:
        >>> word_pattern("abba", "dog cat cat dog")
        True
    """
    words = s.split()
    
    if len(pattern) != len(words):
        return False
    
    char_to_word = {}
    word_to_char = {}
    
    for c, w in zip(pattern, words):
        if c in char_to_word:
            if char_to_word[c] != w:
                return False
        else:
            char_to_word[c] = w
        
        if w in word_to_char:
            if word_to_char[w] != c:
                return False
        else:
            word_to_char[w] = c
    
    return True


# ===== ПОДСЧЁТ СИМВОЛОВ =====

def first_unique_char(s: str) -> int:
    """
    Индекс первого неповторяющегося символа.
    
    Аргументы:
        s: строка
    
    Возвращает:
        int: индекс или -1
    
    Сложность: O(n)
    """
    count = Counter(s)
    
    for i, c in enumerate(s):
        if count[c] == 1:
            return i
    
    return -1


def can_permute_palindrome(s: str) -> bool:
    """
    Можно ли переставить символы строки в палиндром.
    
    Условие: не более одного символа с нечётной частотой.
    
    Сложность: O(n)
    """
    count = Counter(s)
    odd_count = sum(1 for freq in count.values() if freq % 2 == 1)
    return odd_count <= 1


def longest_palindrome(s: str) -> int:
    """
    Максимальная длина палиндрома, который можно построить.
    
    Сложность: O(n)
    """
    count = Counter(s)
    length = 0
    has_odd = False
    
    for freq in count.values():
        length += freq // 2 * 2
        if freq % 2 == 1:
            has_odd = True
    
    return length + 1 if has_odd else length


# ===== ЗАДАЧИ НА СОПОСТАВЛЕНИЕ =====

def can_construct(ransom_note: str, magazine: str) -> bool:
    """
    Можно ли составить ransom_note из букв magazine.
    
    Сложность: O(n + m)
    """
    count = Counter(magazine)
    
    for c in ransom_note:
        if count[c] == 0:
            return False
        count[c] -= 1
    
    return True


def is_anagram(s: str, t: str) -> bool:
    """
    Проверка анаграмм через хеш-таблицу.
    
    Сложность: O(n)
    """
    return Counter(s) == Counter(t)


def find_all_anagrams(s: str, p: str) -> List[int]:
    """
    Найти все индексы начала анаграмм p в строке s.
    
    Использует скользящее окно с хеш-таблицей.
    
    Аргументы:
        s: строка для поиска
        p: паттерн
    
    Возвращает:
        list: начальные индексы всех анаграмм
    
    Сложность: O(n)
    """
    from collections import Counter
    
    result = []
    p_count = Counter(p)
    s_count = Counter()
    len_p = len(p)
    
    for i, c in enumerate(s):
        # Добавляем текущий символ
        s_count[c] += 1
        
        # Удаляем символ за пределами окна
        if i >= len_p:
            left_char = s[i - len_p]
            if s_count[left_char] == 1:
                del s_count[left_char]
            else:
                s_count[left_char] -= 1
        
        # Сравниваем
        if s_count == p_count:
            result.append(i - len_p + 1)
    
    return result


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Собственная HashMap
    print("Собственная HashMap:")
    hm = HashMap()
    hm.put("a", 1)
    hm.put("b", 2)
    hm.put("c", 3)
    print(f"  HashMap: {hm}")
    print(f"  get('a'): {hm.get('a')}")
    print(f"  get('x'): {hm.get('x', 'default')}")
    
    # Two Sum
    print("\nTwo Sum:")
    print(f"  [2, 7, 11, 15], target=9: {two_sum([2, 7, 11, 15], 9)}")
    
    # Подмассивы с суммой
    print("\nПодмассивы с суммой k:")
    print(f"  [1, 1, 1], k=2: {subarray_sum([1, 1, 1], 2)}")
    
    # Группировка анаграмм
    print("\nГруппировка анаграмм:")
    anagrams = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    print(f"  {anagrams}")
    
    # Top K частых
    print("\nTop K частых элементов:")
    print(f"  [1,1,1,2,2,3], k=2: {top_k_frequent([1, 1, 1, 2, 2, 3], 2)}")
    
    # Пересечение множеств
    print("\nПересечение [1,2,2,1] и [2,2]:")
    print(f"  {intersection([1, 2, 2, 1], [2, 2])}")
    
    # Изоморфные строки
    print("\nИзоморфные строки:")
    print(f"  'egg' и 'add': {is_isomorphic('egg', 'add')}")
    print(f"  'foo' и 'bar': {is_isomorphic('foo', 'bar')}")
    
    # Палиндром
    print("\nПалиндром из символов:")
    print(f"  'abccccdd': длина = {longest_palindrome('abccccdd')}")
    
    # Анаграммы в строке
    print("\nАнаграммы 'ab' в 'cbaebabacd':")
    print(f"  индексы: {find_all_anagrams('cbaebabacd', 'ab')}")
