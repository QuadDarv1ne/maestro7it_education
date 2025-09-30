'''
https://codeforces.com/contest/2132/problem/G

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

def solve():
    """
    Эффективное решение с использованием полиномиального хеширования
    для проверки 180° симметрии подматриц.
    """
    import sys
    input = sys.stdin.readline

    MOD = 998244353
    P = [107, 61]
    
    def bin_pow(a, n):
        ret = 1
        while n:
            if n & 1:
                ret = (ret * a) % MOD
            a = (a * a) % MOD
            n >>= 1
        return ret
    
    def add(a, b):
        res = a + b
        return res - MOD if res >= MOD else res
    
    def sub(a, b):
        res = a - b
        return res + MOD if res < 0 else res
    
    def mult(a, b):
        res = a * b
        return res % MOD if res >= MOD else res
    
    # Предвычисляем обратные элементы
    BP = [bin_pow(P[0], MOD - 2), bin_pow(P[1], MOD - 2)]
    
    # Предвычисляем степени
    MAX_SIZE = 1000
    pows = [[], []]
    bpows = [[], []]
    
    for j in range(2):
        pows[j] = [1] * MAX_SIZE
        bpows[j] = [1] * MAX_SIZE
        for i in range(1, MAX_SIZE):
            pows[j][i] = mult(pows[j][i - 1], P[j])
            bpows[j][i] = mult(bpows[j][i - 1], BP[j])
    
    t = int(input())
    while t > 0:
        t -= 1
        n, m = map(int, input().split())
        
        f = []
        for i in range(n):
            f.append(input().strip())
        
        # Прямой хеш
        hash_matrix = [[0] * (m + 2) for _ in range(n + 2)]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cur = mult((ord(f[i - 1][j - 1]) - ord('a') + 1), 
                          mult(pows[0][i - 1], pows[1][j - 1]))
                hash_matrix[i][j] = add(sub(add(hash_matrix[i - 1][j], 
                                              hash_matrix[i][j - 1]), 
                                          hash_matrix[i - 1][j - 1]), cur)
        
        # Обратный хеш (для 180° поворота)
        bhash = [[0] * (m + 2) for _ in range(n + 2)]
        for i in range(n, 0, -1):
            for j in range(m, 0, -1):
                cur = mult((ord(f[i - 1][j - 1]) - ord('a') + 1), 
                          mult(pows[0][n - i], pows[1][m - j]))
                bhash[i][j] = add(sub(add(bhash[i + 1][j], 
                                        bhash[i][j + 1]), 
                                    bhash[i + 1][j + 1]), cur)
        
        def is_palindromic(x1, y1, x2, y2):
            """Проверяет, является ли подматрица палиндромом при 180° повороте"""
            # Прямой хеш подматрицы
            hsh = add(sub(sub(hash_matrix[x2][y2], hash_matrix[x1-1][y2]), 
                         hash_matrix[x2][y1-1]), hash_matrix[x1-1][y1-1])
            
            # Обратный хеш подматрицы
            bhsh = add(sub(sub(bhash[x1][y1], bhash[x2+1][y1]), 
                          bhash[x1][y2+1]), bhash[x2+1][y2+1])
            
            # Нормализуем хеши
            hsh = mult(hsh, mult(bpows[0][x1 - 1], bpows[1][y1 - 1]))
            bhsh = mult(bhsh, mult(bpows[0][n - x2], bpows[1][m - y2]))
            
            return hsh == bhsh
        
        # Находим минимальный прямоугольник
        mn = n * m * 4
        
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Проверяем 4 возможных подматрицы от разных углов
                if is_palindromic(1, 1, i, j):
                    mn = min(mn, (2 * n - i) * (2 * m - j))
                if is_palindromic(1, j, i, m):
                    mn = min(mn, (2 * n - i) * (m + j - 1))
                if is_palindromic(i, 1, n, j):
                    mn = min(mn, (n + i - 1) * (2 * m - j))
                if is_palindromic(i, j, n, m):
                    mn = min(mn, (n + i - 1) * (m + j - 1))
        
        print(mn - m * n)

if __name__ == "__main__":
    solve()

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
    