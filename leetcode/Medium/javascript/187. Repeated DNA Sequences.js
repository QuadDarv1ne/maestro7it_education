/**
 * @param {string} s
 * @return {string[]}
 * 
 * Найти все 10-символьные последовательности ДНК, которые встречаются более одного раза.
 * 
 * @param {string} s Строка, состоящая из символов 'A', 'C', 'G', 'T'
 * @return {string[]} Массив повторяющихся 10-символьных последовательностей
 * 
 * Пример:
 * findRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")
 * // возвращает ["AAAAACCCCC","CCCCCAAAAA"]
 */
var findRepeatedDnaSequences = function(s) {
    if (s.length < 10) return [];
    
    const seen = new Set();
    const repeated = new Set();
    
    for (let i = 0; i <= s.length - 10; i++) {
        const substring = s.substring(i, i + 10);
        
        if (seen.has(substring)) {
            repeated.add(substring);
        } else {
            seen.add(substring);
        }
    }
    
    return Array.from(repeated);
};