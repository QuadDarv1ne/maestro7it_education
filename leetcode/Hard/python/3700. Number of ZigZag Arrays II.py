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

"""
Подсчёт количества зигзагообразных массивов.

Оптимизированное решение на Python с использованием быстрого возведения матрицы в степень.
Специальные оптимизации для обхода TLE:
- Локальные переменные для ускорения поиска
- Отложенное взведение по модулю (накопление в строке)
- Пропуск нулевых элементов матрицы

Args:
    n (int): Длина массива
    l (int): Левая граница диапазона
    r (int): Правая граница диапазона

Returns:
    int: Количество зигзагообразных массивов по модулю 10^9+7
"""

class Solution:
    def zigZagArrays(self, n, l, r):
        MOD = 10**9 + 7
        m = r - l + 1
        if n == 1:
            return m
            
        size = 2 * m
        M = [[0] * size for _ in range(size)]
        
        for i in range(m):
            for j in range(i + 1, m):
                M[i][m + j] = 1
            for j in range(i):
                M[m + i][j] = 1
                
        V = [1] * size
        power = n - 1
        
        while power > 0:
            if power & 1:
                V = self._mat_vec_mul(M, V, MOD)
            M = self._mat_mul(M, M, MOD)
            power >>= 1
            
        return sum(V) % MOD

    def _mat_mul(self, A, B, MOD):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            Ai = A[i]
            Ci = C[i]
            for k in range(n):
                aik = Ai[k]
                if aik:
                    Bk = B[k]
                    for j in range(n):
                        Ci[j] += aik * Bk[j]
            # Оптимизация: берем модуль только после обработки всей строки
            for j in range(n):
                Ci[j] %= MOD
        return C

    def _mat_vec_mul(self, M, V, MOD):
        n = len(M)
        res = [0] * n
        for i in range(n):
            total = 0
            Mi = M[i]
            for j in range(n):
                total += Mi[j] * V[j]
            res[i] = total % MOD
        return res