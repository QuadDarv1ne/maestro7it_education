import math

class Solution:
    def countTriples(self, n):
        """
        Подсчитывает количество упорядоченных троек (a, b, c), 
        где 1 ≤ a, b, c ≤ n и a² + b² = c².
        
        Author: Дулей Максим Игоревич
        ORCID: https://orcid.org/0009-0007-7605-539X
        GitHub: https://github.com/QuadDarv1ne/
        """
        count = 0
        
        for a in range(1, n + 1):
            for b in range(1, n + 1):
                c_sq = a * a + b * b
                c = int(math.sqrt(c_sq))  # Исправлено на совместимый метод
                
                if c <= n and c * c == c_sq:
                    count += 1
        
        return count