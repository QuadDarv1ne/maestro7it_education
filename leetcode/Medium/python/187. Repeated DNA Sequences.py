class Solution(object):
    def findRepeatedDnaSequences(self, s):
        """
        Найти все 10-символьные последовательности ДНК, которые встречаются более одного раза.
        
        Параметры:
        s (str): Строка, состоящая из символов 'A', 'C', 'G', 'T'
        
        Возвращает:
        List[str]: Список повторяющихся 10-символьных последовательностей
        
        Пример:
        >>> solution = Solution()
        >>> solution.findRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")
        ["AAAAACCCCC","CCCCCAAAAA"]
        """
        if len(s) < 10:
            return []
        
        seen = set()
        repeated = set()
        
        for i in range(len(s) - 9):
            substring = s[i:i+10]
            
            if substring in seen:
                repeated.add(substring)
            else:
                seen.add(substring)
        
        return list(repeated)