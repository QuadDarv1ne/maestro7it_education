using System;
using System.Collections.Generic;

public class Solution {
    /**
     * Найти все 10-символьные последовательности ДНК, которые встречаются более одного раза.
     * 
     * @param s Строка, состоящая из символов 'A', 'C', 'G', 'T'
     * @return Список повторяющихся 10-символьных последовательностей
     * 
     * Пример:
     * Solution solution = new Solution();
     * IList<string> result = solution.FindRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT");
     * // result содержит ["AAAAACCCCC","CCCCCAAAAA"]
     */
    public IList<string> FindRepeatedDnaSequences(string s) {
        var result = new List<string>();
        if (s.Length < 10) return result;
        
        var seen = new HashSet<string>();
        var repeated = new HashSet<string>();
        
        for (int i = 0; i <= s.Length - 10; i++) {
            string substring = s.Substring(i, 10);
            
            if (seen.Contains(substring)) {
                repeated.Add(substring);
            } else {
                seen.Add(substring);
            }
        }
        
        result.AddRange(repeated);
        return result;
    }
}