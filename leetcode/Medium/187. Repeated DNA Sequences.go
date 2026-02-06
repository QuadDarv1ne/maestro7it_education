func findRepeatedDnaSequences(s string) []string {
    /**
     * Найти все 10-символьные последовательности ДНК, которые встречаются более одного раза.
     * 
     * @param s Строка, состоящая из символов 'A', 'C', 'G', 'T'
     * @return []string Слайс повторяющихся 10-символьных последовательностей
     * 
     * Пример:
     * result := findRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")
     * // result содержит ["AAAAACCCCC","CCCCCAAAAA"]
     */
    if len(s) < 10 {
        return []string{}
    }
    
    seen := make(map[string]bool)
    repeated := make(map[string]bool)
    
    for i := 0; i <= len(s)-10; i++ {
        substring := s[i:i+10]
        
        if seen[substring] {
            repeated[substring] = true
        } else {
            seen[substring] = true
        }
    }
    
    result := make([]string, 0, len(repeated))
    for seq := range repeated {
        result = append(result, seq)
    }
    
    return result
}