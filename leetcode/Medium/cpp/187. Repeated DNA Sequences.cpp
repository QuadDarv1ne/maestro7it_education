#include <vector>
#include <string>
#include <unordered_set>

using namespace std;

class Solution {
public:
    /**
     * Найти все 10-символьные последовательности ДНК, которые встречаются более одного раза.
     * 
     * @param s Строка, состоящая из символов 'A', 'C', 'G', 'T'
     * @return Вектор повторяющихся 10-символьных последовательностей
     * 
     * Пример:
     * Solution solution;
     * vector<string> result = solution.findRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT");
     * // result содержит ["AAAAACCCCC","CCCCCAAAAA"]
     */
    vector<string> findRepeatedDnaSequences(string s) {
        vector<string> result;
        if (s.length() < 10) return result;
        
        unordered_set<string> seen;
        unordered_set<string> repeated;
        
        for (int i = 0; i <= s.length() - 10; i++) {
            string substring = s.substr(i, 10);
            
            if (seen.find(substring) != seen.end()) {
                repeated.insert(substring);
            } else {
                seen.insert(substring);
            }
        }
        
        // Конвертируем unordered_set в vector
        result.assign(repeated.begin(), repeated.end());
        return result;
    }
};