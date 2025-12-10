'''
LeetCode 3577: Count the Number of Computer Unlocking Permutations
https://leetcode.com/problems/count-the-number-of-computer-unlocking-permutations/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Описание задачи:
Даны n компьютеров с метками от 0 до n-1, каждый с паролем сложности complexity[i].
Компьютер 0 уже разблокирован. Чтобы разблокировать компьютер i, нужен разблокированный 
компьютер j, где j < i и complexity[j] < complexity[i].

Найти количество перестановок [0, 1, 2, ..., n-1], представляющих валидный порядок 
разблокировки компьютеров.

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
'''

from typing import List

class Solution:
    def countPermutations(self, complexity: List[int]) -> int:
        """
        Подсчитывает количество валидных перестановок для разблокировки компьютеров.
        
        Ключевое наблюдение:
        - Компьютер 0 уже разблокирован и имеет сложность complexity[0]
        - Любой другой компьютер i может быть разблокирован ЛЮБЫМ компьютером j,
          где j < i и complexity[j] < complexity[i]
        - Если complexity[i] <= complexity[0], то компьютер i НИКОГДА не сможет быть
          разблокирован (так как 0 < i, но complexity[0] >= complexity[i])
        - Если все компьютеры имеют сложность > complexity[0], то ЛЮБАЯ перестановка
          компьютеров 1..n-1 валидна, так как компьютер 0 (уже разблокирован) может
          разблокировать любой из них
        
        Args:
            complexity (List[int]): Массив сложностей паролей компьютеров
            
        Returns:
            int: Количество валидных перестановок по модулю 10^9 + 7
            
        Examples:
            >>> solution = Solution()
            >>> solution.countPermutations([1, 2, 3])
            2
            Объяснение: Валидные перестановки: [0,1,2] и [0,2,1]
            
            >>> solution.countPermutations([2, 1, 3])
            0
            Объяснение: Компьютер 1 имеет сложность 1 <= 2, не может быть разблокирован
            
        Time Complexity: O(n) - проверяем все компьютеры и вычисляем факториал
        Space Complexity: O(1) - используем только константную память
        """
        MOD = 10**9 + 7
        n = len(complexity)
        
        # Проверяем, можно ли разблокировать все компьютеры
        # Если хотя бы один компьютер имеет сложность <= complexity[0],
        # то его невозможно разблокировать
        for i in range(1, n):
            if complexity[i] <= complexity[0]:
                return 0
        
        # Если все компьютеры имеют сложность > complexity[0],
        # то любая перестановка компьютеров 1..n-1 валидна
        # Количество таких перестановок = (n-1)!
        result = 1
        for i in range(1, n):
            result = (result * i) % MOD
        
        return result