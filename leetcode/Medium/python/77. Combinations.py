'''
LeetCode 77: Combinations
https://leetcode.com/problems/combinations/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Описание задачи:
Даны два целых числа n и k. Вернуть все возможные комбинации из k чисел,
выбранных из диапазона [1, n]. Порядок ответа не имеет значения.

Примеры:
Input: n = 4, k = 2
Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]

Input: n = 1, k = 1
Output: [[1]]

Ограничения:
- 1 <= n <= 20
- 1 <= k <= n

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
'''

# ========================== PYTHON ==========================

class Solution:
    def combine(self, n, k):
        """
        Генерирует все комбинации из k чисел в диапазоне [1, n].
        
        Использует рекурсивный backtracking (возврат назад):
        1. Начинаем с пустой комбинации
        2. Пробуем добавить каждое число от start до n
        3. Рекурсивно строим оставшуюся часть комбинации
        4. Когда длина достигает k, сохраняем комбинацию
        5. Откатываем последний выбор и пробуем следующее число
        
        Time Complexity: O(C(n,k) * k) = O((n! / (k! * (n-k)!)) * k)
        Space Complexity: O(k) для рекурсии
        
        Args:
            n: верхняя граница диапазона [1, n]
            k: количество чисел в комбинации
            
        Returns:
            список всех возможных комбинаций
        """
        result = []
        
        def backtrack(start, path):
            # Базовый случай: комбинация готова
            if len(path) == k:
                result.append(path[:])  # Важно: копируем список!
                return
            
            # Оптимизация: останавливаемся раньше, если недостаточно чисел
            # Нужно еще (k - len(path)) чисел
            # Доступно (n - i + 1) чисел от i до n
            for i in range(start, n + 1):
                # Проверка: хватит ли оставшихся чисел?
                if n - i + 1 < k - len(path):
                    break
                
                # Выбираем число i
                path.append(i)
                
                # Рекурсивно строим остальную часть
                backtrack(i + 1, path)
                
                # Откатываем выбор (backtracking)
                path.pop()
        
        backtrack(1, [])
        return result
