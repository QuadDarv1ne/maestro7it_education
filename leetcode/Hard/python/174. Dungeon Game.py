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

# Python
class Solution:
    """
    Вычисляет минимальное начальное здоровье рыцаря для спасения принцессы.
    Использует обратное динамическое программирование (от конца к началу).
    
    Подход:
    1. Создаём DP таблицу (m+1) x (n+1), заполненную infinity
    2. Базовый случай: dp[m-1][n] = dp[m][n-1] = 1
    3. Идём от правого нижнего угла к левому верхнему
    4. Формула: dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j])
    5. Минимум 1, так как HP должно быть положительным
    
    Сложность по времени: O(m * n)
    Сложность по памяти: O(m * n)
    """
    
    def calculateMinimumHP(self, dungeon):
        m, n = len(dungeon), len(dungeon[0])
        
        # Создаём DP таблицу с дополнительной строкой и столбцом
        dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
        
        # Базовые случаи: перед финальной клеткой нужно иметь хотя бы 1 HP
        dp[m - 1][n] = 1
        dp[m][n - 1] = 1
        
        # Заполняем таблицу от конца к началу
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                # Минимальное HP нужное для следующего хода
                min_hp_next = min(dp[i + 1][j], dp[i][j + 1])
                
                # HP нужное для текущей клетки
                dp[i][j] = max(1, min_hp_next - dungeon[i][j])
        
        return dp[0][0]