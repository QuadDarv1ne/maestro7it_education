import java.util.*;

class Solution {
    /**
     * Найти все 10-символьные последовательности ДНК, которые встречаются более одного раза.
     * 
     * @param s Строка, состоящая из символов 'A', 'C', 'G', 'T'
     * @return Список повторяющихся 10-символьных последовательностей
     * 
     * Пример:
     * Solution solution = new Solution();
     * List<String> result = solution.findRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT");
     * // result содержит ["AAAAACCCCC","CCCCCAAAAA"]
     */
    public List<String> findRepeatedDnaSequences(String s) {
        List<String> result = new ArrayList<>();
        if (s.length() < 10) return result;
        
        Set<String> seen = new HashSet<>();
        Set<String> repeated = new HashSet<>();
        
        for (int i = 0; i <= s.length() - 10; i++) {
            String substring = s.substring(i, i + 10);
            
            if (seen.contains(substring)) {
                repeated.add(substring);
            } else {
                seen.add(substring);
            }
        }
        
        result.addAll(repeated);
        return result;
    }
}