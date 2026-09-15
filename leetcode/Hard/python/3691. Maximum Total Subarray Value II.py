"""
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
"""

import heapq

class SparseTableRMQ:
    """
    Разреженная таблица (Sparse Table) для быстрых запросов
    минимума и максимума на отрезке за O(1).
    
    Предподсчёт: O(n log n)
    Запрос: O(1)
    Память: O(n log n)
    
    Автор: Дуплей Максим Игоревич
    """
    def __init__(self, data):
        self.n = len(data)
        self.max_log = self.n.bit_length() + 1
        self.f_max = [[0] * self.max_log for _ in range(self.n)]
        self.f_min = [[0] * self.max_log for _ in range(self.n)]
        
        self.lg = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.lg[i] = self.lg[i >> 1] + 1
        
        for i in range(self.n):
            self.f_max[i][0] = data[i]
            self.f_min[i][0] = data[i]
        
        for j in range(1, self.max_log):
            step = 1 << (j - 1)
            for i in range(self.n - (1 << j) + 1):
                self.f_max[i][j] = max(
                    self.f_max[i][j - 1],
                    self.f_max[i + step][j - 1]
                )
                self.f_min[i][j] = min(
                    self.f_min[i][j - 1],
                    self.f_min[i + step][j - 1]
                )
    
    def query_max(self, l, r):
        """Возвращает максимум на отрезке [l, r]."""
        k = self.lg[r - l + 1]
        return max(
            self.f_max[l][k],
            self.f_max[r - (1 << k) + 1][k]
        )
    
    def query_min(self, l, r):
        """Возвращает минимум на отрезке [l, r]."""
        k = self.lg[r - l + 1]
        return min(
            self.f_min[l][k],
            self.f_min[r - (1 << k) + 1][k]
        )


class Solution:
    def maxTotalValue(self, nums, k):
        """
        Находит максимальную суммарную ценность k подмассивов.
        
        Ценность подмассива = max - min. Для каждого левого края l
        ценность монотонно возрастает с ростом правого края r.
        
        Алгоритм:
        1. Строим ST-таблицу для O(1) запросов min/max
        2. Для каждого l помещаем в max-кучу подмассив [l, n-1]
        3. k раз извлекаем максимум и добавляем в кучу [l, r-1]
        
        Args:
            nums: Массив целых чисел
            k: Количество выбираемых подмассивов
            
        Returns:
            Максимальная суммарная ценность k подмассивов
            
        Сложность:
            Время: O(n log n + k log n)
            Память: O(n log n)
        
        Автор: Дуплей Максим Игоревич
        """
        n = len(nums)
        st = SparseTableRMQ(nums)
        
        # Max-куча: (-ценность, l, r)
        pq = []
        for l in range(n):
            val = st.query_max(l, n - 1) - st.query_min(l, n - 1)
            heapq.heappush(pq, (-val, l, n - 1))
        
        ans = 0
        for _ in range(k):
            neg_val, l, r = heapq.heappop(pq)
            ans += -neg_val
            if r > l:
                val = st.query_max(l, r - 1) - st.query_min(l, r - 1)
                heapq.heappush(pq, (-val, l, r - 1))
        
        return ans