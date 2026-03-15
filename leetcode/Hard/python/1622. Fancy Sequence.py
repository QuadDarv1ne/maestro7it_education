'''
https://leetcode.com/problems/permutation-sequence/description/
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

class Fancy:
    """
    Класс Fancy управляет последовательностью целых чисел с массовыми операциями.
    Поддерживает добавление, массовое сложение, массовое умножение и запрос по индексу.
    Все вычисления производятся по модулю 1_000_000_007.
    """

    def __init__(self):
        """
        Конструктор. Инициализирует пустую последовательность.
        Устанавливает начальные значения: mul = 1, add = 0.
        """
        self.seq = []
        self.mul = 1
        self.add = 0
        self.MOD = 10**9 + 7

    def _mod_pow(self, a, b):
        """Вспомогательный метод: быстрое возведение в степень по модулю."""
        res = 1
        while b:
            if b & 1:
                res = res * a % self.MOD
            a = a * a % self.MOD
            b >>= 1
        return res

    def _mod_inv(self, a):
        """Вспомогательный метод: обратный элемент по модулю (теорема Ферма)."""
        return self._mod_pow(a, self.MOD - 2)

    def append(self, val):
        """
        Добавляет число val в конец последовательности.
        Сохраняет "сырое" значение, скорректированное с учётом текущих mul и add.
        
        Аргументы:
            val: целое число для добавления
        """
        # raw = (val - add) * inv(mul) mod MOD
        raw = (val - self.add) % self.MOD
        raw = raw * self._mod_inv(self.mul) % self.MOD
        self.seq.append(raw)

    def addAll(self, inc):
        """
        Увеличивает все существующие значения в последовательности на inc.
        Обновляет только глобальную переменную add.
        
        Аргументы:
            inc: число, на которое увеличиваются все элементы
        """
        self.add = (self.add + inc) % self.MOD

    def multAll(self, m):
        """
        Умножает все существующие значения в последовательности на m.
        Обновляет глобальные переменные mul и add.
        
        Аргументы:
            m: множитель для всех элементов
        """
        self.mul = self.mul * m % self.MOD
        self.add = self.add * m % self.MOD

    def getIndex(self, idx):
        """
        Возвращает текущее значение элемента по индексу idx (0-базовый).
        Вычисляется как seq[idx] * mul + add по модулю MOD.
        Если индекс вне диапазона, возвращает -1.
        
        Аргументы:
            idx: индекс запрашиваемого элемента
            
        Возвращает:
            значение элемента или -1
        """
        if idx >= len(self.seq):
            return -1
        return (self.seq[idx] * self.mul + self.add) % self.MOD